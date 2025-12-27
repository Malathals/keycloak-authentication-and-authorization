from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class RegisterBody(BaseModel):
    username: str = Field(min_length=3)
    email: EmailStr
    password: str = Field(min_length=8)
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class LoginBody(BaseModel):
    email: EmailStr
    password: str


class MeResponse(BaseModel):
    sub: Optional[str] = None
    username: Optional[str] = None
    email: Optional[str] = None
    roles: list[str] = []