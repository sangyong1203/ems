import type { APIResponse } from '@/http/type'

// 로그인 입력
export type SigninParams = {
    username: string // 로그인 ID
    password: string // 입력 비밀번호
}

// 서버가 발급한 관리자 인증 토큰
export type SessionTokens = {
    accessToken: string // 액세스 토큰
    refreshToken: string // 갱신 토큰
}

// 인증된 관리자 정보
export type UserInfo = {
    id: number // 사용자 ID
    username: string // 로그인 ID
    email: string // 이메일
    name: string // 표시 이름
    role: 'Platform Admin' // 로그인 가능한 역할
    userLevel: 'PLATFORM_ADMIN' // 프론트 메뉴 권한
    landingPage: string // 로그인 후 진입 경로
}

// 현재 비밀번호 재확인을 포함한 변경 요청
export type ChangePasswordParams = {
    currentPassword: string // 현재 비밀번호
    newPassword: string // 새 비밀번호 (8~128자)
}

export type SigninResponse = APIResponse<SessionTokens & { landingPage: string; user: UserInfo }> // 로그인 응답
export type UserInfoResponse = APIResponse<UserInfo> // 현재 사용자 응답
