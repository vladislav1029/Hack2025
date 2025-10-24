from typing import Optional
from src.core.models.role import Role


from pydantic import BaseModel, EmailStr


import uuid
from datetime import datetime


class UserResponse(BaseModel):
    oid: uuid.UUID
    email: EmailStr
    is_active: bool
    is_verificate: bool
    role: Role
    created_at: datetime
    update_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserRegister(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class AuthResponse(BaseModel):
    user: UserResponse
    access_token: str
    token_type: str = "bearer"
