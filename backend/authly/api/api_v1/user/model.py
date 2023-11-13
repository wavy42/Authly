from typing import Optional


from backend.authly.core.config import application_config
from authly.api.api_v1.authentication import base64_password
from pydantic import BaseModel, EmailStr, Field, constr, validator

config_password_min_length = (
    application_config.PasswordConfig.DEFAULT_PASSWORD_MIN_LENGTH
)
config_password_max_length = (
    application_config.PasswordConfig.DEFAULT_PASSWORD_MAX_LENGTH
)


class UserRegistration(BaseModel):
    email: EmailStr = Field(..., example="1337@Allah.com")
    username: str = Field(..., example="abc#1234")
    password: constr(
        min_length=config_password_min_length,
        max_length=config_password_max_length,
    ) = Field(..., example="XDFmYyciU3wreHUnOCwiX3VXajMkS1BeKQ==")

    @validator("password")
    def validate_password(cls, value):
        return base64_password.validate_base64_password(value)

    def json(self, *args, **kwargs):
        self.password = base64_password.encode_to_base64(self.password)
        return dict(self)


class LoginRequest(BaseModel):
    email: Optional[EmailStr]
    user_id: Optional[str]
    password: str

    @validator("password")
    def validate_password(cls, value):
        return base64_password.validate_base64_password(value)


class Token(BaseModel):
    access_token: str
    token_type: str


class User(BaseModel):
    id: str
    username: str | None = None
    email: str | None = None
    disabled: bool | None = None


class UpdateUserEmail(BaseModel):
    oldEmail: str
    email: str
