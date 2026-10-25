import type { APIResponse } from '@/http/type'

// UserStatus 사용자 활성 상태
export type UserStatus = 'Active' | 'Inactive' | 'Locked'

// UserRole 사용자 권한 역할
export type UserRole = 'Platform Admin' | 'Operator' | 'Viewer'

// UserItem 사용자 상세 정보
export type UserItem = {
    id: number // 사용자 ID
    name: string // 사용자 이름
    email: string // 이메일 주소
    department: string // 소속 부서
    role: UserRole // 권한 역할
    status: UserStatus // 계정 상태
    lastLoginAt: string // 최근 로그인 일시
    createdAt: string // 계정 생성 일시
}

// RequestParams 사용자 목록 조회 파라미터
export type RequestParams = {
    keyword: string // 검색 키워드 (이름/이메일/부서)
    role: UserRole | '' // 권한 필터
    status: UserStatus | '' // 계정 상태 필터
    pageNumber: number // 페이지 번호
    pageSize: number // 페이지 크기
}

// UserSaveParams 사용자 등록/수정 파라미터
export type UserSaveParams = Pick<UserItem, 'name' | 'email' | 'department' | 'role' | 'status'> & {
    password?: string // 신규 등록 시 필수; 수정 시 입력하면 비밀번호와 기존 세션을 재설정
}

// UserListResponse 사용자 목록 응답
export type UserListResponse = APIResponse & {
    data: {
        list: UserItem[] // 사용자 목록
        totalCount: number // 총 건수
    }
}

// UserSaveResponse 사용자 정보 저장 응답
export type UserSaveResponse = APIResponse<UserItem>

// UserDeleteResponse 사용자 삭제 응답
export type UserDeleteResponse = APIResponse<{ result: string }>
