import hashlib

from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerificationError


password_hasher = PasswordHasher()  # 무작위 salt를 사용하는 Argon2id 해시 생성기
DUMMY_PASSWORD_HASH = password_hasher.hash('unused-login-timing-check')  # 없는 계정도 해시 검증 비용을 동일하게 적용


# 비밀번호를 평문으로 저장하지 않고 Argon2id 해시를 생성합니다.
def hash_password(password: str) -> str:
    return password_hasher.hash(password)


# Argon2 해시만 검증하며 평문 비교나 다른 형식의 대체 검증을 허용하지 않습니다.
def verify_password(encoded: str, password: str) -> bool:
    try:
        return password_hasher.verify(encoded, password)
    except (VerificationError, InvalidHashError):
        return False


# DB에는 토큰 원문 대신 SHA-256 해시를 저장합니다.
def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode('utf-8')).hexdigest()
