import asyncio
import json
import os
import sys
import unittest
from datetime import timedelta
from unittest.mock import patch
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from fastapi import FastAPI
from fastapi.routing import APIRoute
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.api.router import api_router
from app.core.database import Base, get_db
from app.db.init_db import _ensure_admin_users
from app.domains.auth.dependencies import utc_now
from app.domains.auth.models import AuthSession, User
from app.domains.auth.security import hash_password, hash_token, verify_password

PASSWORD = 'Test-password-2026!'
PASSWORD_HASH = hash_password(PASSWORD)


# 추가 HTTP 패키지 없이 ASGI 앱에 JSON 요청을 전달하고 상태 코드와 응답을 수집합니다.
async def asgi_request(app, method, path, body=None, token=None):
    data = json.dumps(body).encode() if body is not None else b''
    headers = [(b'content-type', b'application/json')]
    if token:
        headers.append((b'authorization', ('Bearer ' + token).encode()))
    scope = {'type': 'http', 'asgi': {'version': '3.0'}, 'http_version': '1.1', 'method': method,
             'scheme': 'http', 'path': path, 'raw_path': path.encode(), 'root_path': '',
             'query_string': b'', 'headers': headers, 'client': ('127.0.0.1', 1234), 'server': ('test', 80)}
    messages = []
    # ASGI 앱에 요청 본문을 전달합니다.
    async def receive():
        return {'type': 'http.request', 'body': data, 'more_body': False}
    # ASGI 응답 메시지를 수집합니다.
    async def send(message):
        messages.append(message)
    await app(scope, receive, send)
    status = next(m['status'] for m in messages if m['type'] == 'http.response.start')
    payload = b''.join(m.get('body', b'') for m in messages if m['type'] == 'http.response.body')
    return status, json.loads(payload) if payload else None


class AuthenticationTests(unittest.TestCase):
    # 실제 DB와 분리된 메모리 DB 및 요청별 세션을 준비합니다.
    def setUp(self):
        self.engine = create_engine('sqlite://', connect_args={'check_same_thread': False}, poolclass=StaticPool)
        Base.metadata.create_all(self.engine)
        self.sessions = sessionmaker(bind=self.engine, autoflush=False)
        with self.sessions() as db:
            db.add_all([
                User(username='admin', password_hash=PASSWORD_HASH, name='Actual Admin', email='actual@example.com', department='Test', role='Platform Admin', status='Active'),
                User(username='operator', password_hash=PASSWORD_HASH, name='Operator', email='operator@example.com', department='Test', role='Operator', status='Active'),
            ])
            db.commit()
        self.app = FastAPI()
        self.app.include_router(api_router)
        def test_db():
            with self.sessions() as db:
                try:
                    yield db
                except Exception:
                    db.rollback()
                    raise
        self.app.dependency_overrides[get_db] = test_db

    # 검증에 사용한 메모리 DB 연결을 해제합니다.
    def tearDown(self):
        self.engine.dispose()

    # 테스트 요청을 독립 이벤트 루프에서 실행합니다.
    def request(self, method, path, body=None, token=None):
        return asyncio.run(asgi_request(self.app, method, path, body, token))

    # 관리자 로그인 성공을 확인하고 발급된 토큰을 반환합니다.
    def login(self, username='admin', password=PASSWORD):
        status, response = self.request('POST', '/api/auth/login', {'username': username, 'password': password})
        self.assertEqual(status, 200)
        self.assertEqual(response['result'], 'SUCCESS')
        return response['data']

    # 실제 사용자 정보, 토큰 해시 저장과 만료 기간을 확인합니다.
    def test_real_identity_and_hash_only_storage(self):
        tokens = self.login()
        status, response = self.request('GET', '/api/auth/me', token=tokens['accessToken'])
        self.assertEqual(status, 200)
        self.assertEqual(response['data']['name'], 'Actual Admin')
        self.assertEqual(response['data']['email'], 'actual@example.com')
        self.assertNotIn('password_hash', response['data'])
        with self.sessions() as db:
            session = db.query(AuthSession).one()
            self.assertEqual(session.access_token_hash, hash_token(tokens['accessToken']))
            self.assertNotEqual(session.refresh_token_hash, tokens['refreshToken'])
            self.assertEqual(session.refresh_expires_at - session.created_at, timedelta(days=1))
            self.assertEqual(session.access_expires_at - session.created_at, timedelta(hours=1))

    # 틀린 비밀번호·미등록·비활성·비관리자 계정의 로그인 차단을 확인합니다.
    def test_login_rejects_wrong_unknown_inactive_and_nonadmin(self):
        for name, password in [('admin', 'wrong'), ('missing', PASSWORD)]:
            status, response = self.request('POST', '/api/auth/login', {'username': name, 'password': password})
            self.assertEqual(status, 200)
            self.assertEqual(response['result'], 'LOGIN_FAILED')
        status, _ = self.request('POST', '/api/auth/login', {'username': 'operator', 'password': PASSWORD})
        self.assertEqual(status, 403)
        with self.sessions() as db:
            db.query(User).filter(User.username == 'admin').update({'status': 'Locked'})
            db.commit()
        self.assertEqual(self.request('POST', '/api/auth/login', {'username': 'admin', 'password': PASSWORD})[1]['result'], 'LOGIN_FAILED')

    # 로그인에서 평문 비밀번호 저장값을 대체 검증하지 않는지 확인합니다.
    def test_plaintext_is_not_accepted_at_login(self):
        with self.sessions() as db:
            db.query(User).filter(User.username == 'admin').update({'password_hash': PASSWORD})
            db.commit()
        self.assertEqual(self.request('POST', '/api/auth/login', {'username': 'admin', 'password': PASSWORD})[1]['result'], 'LOGIN_FAILED')

    # 모든 업무 API와 기존 고정 토큰의 인증 우회 차단을 확인합니다.
    def test_every_business_route_requires_auth(self):
        count = 0
        for route in self.app.routes:
            if not isinstance(route, APIRoute) or not route.path.startswith('/api/') or route.path.startswith('/api/auth/'):
                continue
            path = route.path
            for parameter in route.param_convertors:
                path = path.replace('{' + parameter + '}', '1')
            method = next(iter(route.methods))
            status, _ = self.request(method, path, {} if method in {'POST', 'PUT'} else None)
            self.assertEqual(status, 401, (method, path))
            count += 1
        self.assertGreater(count, 40)
        self.assertEqual(self.request('GET', '/api/auth/me', token='solar-ems-local-access-token')[0], 401)
        self.assertEqual(self.request('POST', '/api/auth/reissue', {'refreshToken': 'solar-ems-local-refresh-token'})[0], 401)
        self.assertEqual(self.request('POST', '/api/auth/logout', {'refreshToken': 'solar-ems-local-refresh-token'})[0], 200)

    # 토큰 교체 후 기존 액세스·갱신 토큰이 재사용되지 않는지 확인합니다.
    def test_rotation_invalidates_old_access_and_refresh(self):
        old = self.login()
        status, response = self.request('POST', '/api/auth/reissue', {'refreshToken': old['refreshToken']})
        self.assertEqual(status, 200)
        new = response['data']
        self.assertNotEqual(old['refreshToken'], new['refreshToken'])
        self.assertEqual(self.request('POST', '/api/auth/reissue', {'refreshToken': old['refreshToken']})[0], 401)
        self.assertEqual(self.request('GET', '/api/auth/me', token=old['accessToken'])[0], 401)
        self.assertEqual(self.request('GET', '/api/auth/me', token=new['accessToken'])[0], 200)

    # 액세스 만료 시 갱신과 세션 절대 만료 시 차단을 확인합니다.
    def test_access_expiry_allows_refresh_but_session_expiry_does_not(self):
        tokens = self.login()
        with self.sessions() as db:
            db.query(AuthSession).update({'access_expires_at': utc_now() - timedelta(seconds=1)})
            db.commit()
        self.assertEqual(self.request('GET', '/api/auth/me', token=tokens['accessToken'])[0], 401)
        status, response = self.request('POST', '/api/auth/reissue', {'refreshToken': tokens['refreshToken']})
        self.assertEqual(status, 200)
        with self.sessions() as db:
            db.query(AuthSession).update({'refresh_expires_at': utc_now() - timedelta(seconds=1)})
            db.commit()
        self.assertEqual(self.request('POST', '/api/auth/reissue', {'refreshToken': response['data']['refreshToken']})[0], 401)
        self.assertEqual(self.request('GET', '/api/auth/me', token=response['data']['accessToken'])[0], 401)

    # 토큰 교체 직전에 시작한 로그아웃도 교체된 세션을 폐기하는지 확인합니다.
    def test_logout_with_just_rotated_refresh_token(self):
        old = self.login()
        status, response = self.request('POST', '/api/auth/reissue', {'refreshToken': old['refreshToken']})
        self.assertEqual(status, 200)
        self.assertEqual(self.request('POST', '/api/auth/logout', {'refreshToken': old['refreshToken']})[0], 200)
        self.assertEqual(self.request('GET', '/api/auth/me', token=response['data']['accessToken'])[0], 401)
        self.assertEqual(self.request('POST', '/api/auth/reissue', {'refreshToken': response['data']['refreshToken']})[0], 401)

    # 로그아웃 재요청과 양쪽 토큰의 폐기를 확인합니다.
    def test_logout_revokes_both_tokens(self):
        tokens = self.login()
        for _ in range(2):
            self.assertEqual(self.request('POST', '/api/auth/logout', {'refreshToken': tokens['refreshToken']})[0], 200)
        self.assertEqual(self.request('GET', '/api/auth/me', token=tokens['accessToken'])[0], 401)
        self.assertEqual(self.request('POST', '/api/auth/reissue', {'refreshToken': tokens['refreshToken']})[0], 401)

    # 현재 비밀번호 재확인과 변경 후 모든 세션 폐기를 확인합니다.
    def test_password_change_checks_current_and_revokes_all_sessions(self):
        tokens, other = self.login(), self.login()
        self.assertEqual(self.request('POST', '/api/auth/password/change', {'currentPassword': 'wrong', 'newPassword': 'New-password-2026!'}, tokens['accessToken'])[0], 400)
        self.assertEqual(self.request('GET', '/api/auth/me', token=tokens['accessToken'])[0], 200)
        self.assertEqual(self.request('POST', '/api/auth/password/change', {'currentPassword': PASSWORD, 'newPassword': 'New-password-2026!'}, tokens['accessToken'])[0], 200)
        for session in (tokens, other):
            self.assertEqual(self.request('GET', '/api/auth/me', token=session['accessToken'])[0], 401)
            self.assertEqual(self.request('POST', '/api/auth/reissue', {'refreshToken': session['refreshToken']})[0], 401)
        self.login(password='New-password-2026!')

    # 기존 검증 토큰 방식과 이메일 재설정이 차단되는지 확인합니다.
    def test_legacy_verification_bypass_and_email_reset_disabled(self):
        tokens = self.login()
        status, _ = self.request('POST', '/api/auth/password/change', {'verificationToken': 'solar-ems-local-verification-token', 'newPassword': 'New-password-2026!'}, tokens['accessToken'])
        self.assertEqual(status, 422)
        for method in ('POST', 'PUT'):
            self.assertEqual(self.request(method, '/api/auth/password/reset', {})[0], 403)

    # 초기 비밀번호 필수 입력·해시 저장·중복 사용자 처리를 확인합니다.
    def test_initial_password_required_and_hash_stored(self):
        tokens = self.login()
        payload = {'name': 'New Admin', 'email': 'new@example.com', 'department': 'Test', 'role': 'Platform Admin', 'status': 'Active'}
        self.assertEqual(self.request('POST', '/api/users', payload, tokens['accessToken'])[0], 422)
        payload['password'] = PASSWORD
        status, response = self.request('POST', '/api/users', payload, tokens['accessToken'])
        self.assertEqual(status, 200)
        self.assertNotIn('password', response['data'])
        with self.sessions() as db:
            user = db.query(User).filter(User.username == 'new@example.com').one()
            self.assertNotEqual(user.password_hash, PASSWORD)
            self.assertTrue(verify_password(user.password_hash, PASSWORD))
        self.login('new@example.com')
        self.assertEqual(self.request('POST', '/api/users', payload, tokens['accessToken'])[0], 409)

    # 마지막 활성 관리자의 삭제·권한 변경 차단을 확인합니다.
    def test_last_admin_cannot_be_deleted_or_demoted(self):
        tokens = self.login()
        self.assertEqual(self.request('DELETE', '/api/users/1', token=tokens['accessToken'])[0], 409)
        payload = {'name': 'Admin', 'email': 'actual@example.com', 'department': 'Test', 'role': 'Viewer', 'status': 'Active'}
        self.assertEqual(self.request('PUT', '/api/users/1', payload, tokens['accessToken'])[0], 409)

    # 관리자에 의한 사용자 비밀번호 재설정과 기존 세션 폐기를 확인합니다.
    def test_user_update_revokes_sessions_and_password_reset_works(self):
        tokens = self.login()
        payload = {'name': 'Second', 'email': 'second@example.com', 'department': 'Test', 'role': 'Platform Admin', 'status': 'Active', 'password': PASSWORD}
        status, response = self.request('POST', '/api/users', payload, tokens['accessToken'])
        self.assertEqual(status, 200)
        other = self.login('second@example.com')
        payload['password'] = 'Replacement-password!'
        self.assertEqual(self.request('PUT', '/api/users/' + str(response['data']['id']), payload, tokens['accessToken'])[0], 200)
        self.assertEqual(self.request('GET', '/api/auth/me', token=other['accessToken'])[0], 401)
        self.login('second@example.com', 'Replacement-password!')

    # 발급 후에도 변경된 역할과 계정 상태가 즉시 반영되는지 확인합니다.
    def test_role_and_status_checked_on_every_request(self):
        tokens = self.login()
        with self.sessions() as db:
            db.query(User).filter(User.username == 'admin').update({'role': 'Viewer'})
            db.commit()
        self.assertEqual(self.request('GET', '/api/users', token=tokens['accessToken'])[0], 403)
        self.assertEqual(self.request('POST', '/api/auth/reissue', {'refreshToken': tokens['refreshToken']})[0], 403)
        with self.sessions() as db:
            db.query(User).filter(User.username == 'admin').update({'status': 'Inactive'})
            db.commit()
        self.assertEqual(self.request('GET', '/api/auth/me', token=tokens['accessToken'])[0], 401)

    # 기본 관리자 전환의 환경변수 요구와 기존 해시 유지 동작을 확인합니다.
    def test_bootstrap_requires_env_and_migrates_only_once(self):
        with self.sessions() as db:
            db.query(User).filter(User.username == 'admin').update({'password_hash': '1111'})
            db.commit()
            with patch.dict(os.environ, {}, clear=True):
                with self.assertRaises(RuntimeError):
                    _ensure_admin_users(db)
            with patch.dict(os.environ, {'INITIAL_ADMIN_PASSWORD': PASSWORD}):
                _ensure_admin_users(db)
                db.commit()
            user = db.query(User).filter(User.username == 'admin').one()
            self.assertTrue(verify_password(user.password_hash, PASSWORD))
            encoded = user.password_hash
            with patch.dict(os.environ, {'INITIAL_ADMIN_PASSWORD': 'Different-password!'}):
                _ensure_admin_users(db)
                db.commit()
            self.assertEqual(user.password_hash, encoded)

    # 빈 DB에서 샘플 계정 없이 관리자만 생성되는지 확인합니다.
    def test_fresh_bootstrap_creates_only_admin(self):
        with self.sessions() as db:
            db.query(User).delete()
            db.commit()
            with patch.dict(os.environ, {'INITIAL_ADMIN_PASSWORD': PASSWORD}):
                _ensure_admin_users(db)
                db.commit()
            self.assertEqual(db.query(User).count(), 1)
            self.assertEqual(db.query(User).one().role, 'Platform Admin')

    # 실제 시작 이벤트가 새 관리자와 세션 테이블을 준비하고 인증 API와 연결되는지 격리 DB에서 확인합니다.
    def test_full_startup_initializes_auth_and_issues_tokens(self):
        from app.main import startup_event
        with self.sessions() as db:
            db.query(User).delete()
            db.commit()
        with patch('app.db.init_db.engine', self.engine), patch('app.main.SessionLocal', self.sessions), patch.dict(os.environ, {'INITIAL_ADMIN_PASSWORD': PASSWORD}):
            startup_event()
        tokens = self.login()
        self.assertEqual(self.request('GET', '/api/project', token=tokens['accessToken'])[0], 200)
        self.assertEqual(self.request('GET', '/api/power-flow/editor', token=tokens['accessToken'])[0], 200)


if __name__ == '__main__':
    unittest.main(verbosity=2)
