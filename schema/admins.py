from pydantic import BaseModel, EmailStr, field_validator


class AdminRegister(BaseModel):
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


class AdminRegisterResponse(BaseModel):
    email: EmailStr
    name: str
    phone: str
    address: str
    city: str
    state: str
    address: str
    username: str


class GetAdminDetail(BaseModel):
    access_token: str


class VerifyAdminEmail(BaseModel):
    username: str
    code: str

    @field_validator('code')
    def code_validator(cls, value):
        if len(value) < 6 or len(value) > 6:
            raise ValueError('Code must be at least 6 characters long')
        return value


class UpdateSuperUser(BaseModel):
    is_superuser: bool
    access_token: str


class AdminDetailResponse(BaseModel):
    username: str
    name: str
    email: str
    is_superuser: bool
    phone: str
    address: str

    # @field_validator('is_superuser')
    # def is_superuser(cls, value):
    #     print(value)
    #     if value == '1':
    #         return True
    #     else:
    #         return False
