from pydantic import BaseModel, EmailStr, field_validator, ValidationError, validator


class UserRegister(BaseModel):
    email: EmailStr
    name: str
    phone: str
    address: str
    password: str
    confirm_password: str
    city: str
    state: str
    address: str
    username: str

    @field_validator('password')
    def password_validator(cls, value, values):
        if len(value) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return value

    @field_validator('confirm_password')
    def passwords_match(cls, value, values):
        if value != values.data.get('password'):
            raise ValueError('Password and confirm password do not match')
        return value


class UserRegisterResponse(BaseModel):
    email: EmailStr
    name: str
    phone: str
    address: str
    city: str
    state: str
    address: str
    username: str


class VerifyEmail(BaseModel):
    username: str
    code: str

    @field_validator('code')
    def code_validator(cls, value):
        if len(value) < 6 or len(value) > 6:
            raise ValueError('Code must be at least 6 characters long')
        return value


class Login(BaseModel):
    username: str
    password: str

    @field_validator('password')
    def password_validator(cls, value, values):
        if len(value) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return value


class GetUserDetail(BaseModel):
    access_token: str


class UserDetailResponse(BaseModel):
    username: str
    email: str
    phone: str
    address: str


class NewAccessToken(BaseModel):
    refresh_token: str


class NewAccessTokenResponse(BaseModel):
    access_token: str


class Logout(BaseModel):
    access_token: str


class ChangePassword(BaseModel):
    current_password: str
    new_password: str
    confirm_password: str
    access_token: str

    @field_validator('new_password')
    def current_password_validator(cls, value):
        if len(value) < 8:
            raise ValueError('Current password must be at least 8 characters long')
        return value

    @field_validator('confirm_password')
    def passwords_match(cls, value, values):
        if value != values.data.get('new_password'):
            raise ValueError('Password and confirm password do not match')
        return value


class UpdateEmail(BaseModel):
    email: EmailStr
    access_token: str


class UpdateName(BaseModel):
    name: str
    access_token: str


class UpdatePhone(BaseModel):
    phone: str
    access_token: str


class UpdateAddress(BaseModel):
    address: str
    access_token: str


class UpdateUserName(BaseModel):
    username: str
    access_token: str


class ForgetPassword(BaseModel):
    username: str


class ForgetPasswordConfirm(BaseModel):
    password: str
    confirm_password: str
    code: str
    username: str

    @field_validator('password')
    def password_validator(cls, value):
        if len(value) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return value

    @field_validator('confirm_password')
    def passwords_match(cls, value, values):
        if value != values.data.get('password'):
            raise ValueError('Password and confirm password do not match')
        return value
