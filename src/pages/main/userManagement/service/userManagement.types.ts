import type { APIResponse } from '@/http/type'

export type UserStatus = 'Active' | 'Inactive' | 'Locked'

export type UserRole = 'Platform Admin' | 'Operator' | 'Viewer'

export type UserItem = {
    id: number
    name: string
    email: string
    department: string
    role: UserRole
    status: UserStatus
    lastLoginAt: string
    createdAt: string
}

export type RequestParams = {
    keyword: string
    role: UserRole | ''
    status: UserStatus | ''
    pageNumber: number
    pageSize: number
}

export type UserSaveParams = Pick<UserItem, 'name' | 'email' | 'department' | 'role' | 'status'>

export type UserListResponse = APIResponse & {
    data: {
        list: UserItem[]
        totalCount: number
    }
}

export type UserSaveResponse = APIResponse<UserItem>

export type UserDeleteResponse = APIResponse<{ result: string }>
