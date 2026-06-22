import type { APIResponse } from '@/http/type'

export type ChangePassword = {
    newPassword: string
    newPasswordConfirm: string
}

export type SigninParams = {
    username: string
    password: string
}

export type ChangePasswordParams = {
    newPassword: string
    verificationToken: string
    isAdmin: string
}

export type PasswordResetRequestParams = {
    email: string
    requestType?: string
    isAdmin?: string
}

export type ResetPasswordParams = {
    password: string
    requestType: string
    isAdmin: string
    verificationToken: string
}

export type UserInfo = {
    email?: string
    krName?: string
    name?: string
    userLevel?: string
    landingPage?: string
}

export type UserInfoResponse = APIResponse<UserInfo>
