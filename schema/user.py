from pydantic import BaseModel, EmailStr, field_validator, ValidationError


class UserRegister(BaseModel):
    email: EmailStr
    name: str
    phone: str
    address: str
    password: str
    confirm_password: str
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


class VerifyEmail(BaseModel):
    username: str
    code: str

    @field_validator('code')
    def code_validator(cls, value):
        if len(value) < 6:
            raise ValueError('Code must be at least 8 characters long')
        return value


class Login(BaseModel):
    username: str
    password: str

    @field_validator('password')
    def password_validator(cls, value, values):
        if len(value) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return value
