from pydantic import BaseModel, EmailStr, Field


class RegisterBody(BaseModel):
    username: str = Field(min_length=3)
    email: EmailStr
    password: str = Field(min_length=8)
    first_name: str | None = None
    last_name: str | None = None


class LoginBody(BaseModel):
    username: str
    password: str


class MeResponse(BaseModel):
    sub: str | None = None
    username: str | None = None
    email: str | None = None
    roles: list[str] = []