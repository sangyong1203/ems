from pydantic import BaseModel


class LoginBody(BaseModel):
    username: str
    password: str


class PasswordChangeBody(BaseModel):
    newPassword: str
    verificationToken: str | None = None
    isAdmin: str | None = None


class PasswordResetRequestBody(BaseModel):
    email: str
    requestType: str | None = None
    isAdmin: str | None = None


class PasswordResetBody(BaseModel):
    password: str
    requestType: str | None = None
    isAdmin: str | None = None
    verificationToken: str | None = None


class TokenReissueBody(BaseModel):
    refreshToken: str | None = None
    isAdmin: str | None = None


class UserSaveBody(BaseModel):
    name: str
    email: str
    department: str
    role: str
    status: str
