from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional
from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"

# data from api client
class UserCreate(BaseModel):
    full_name: str = Field(..., min_length=1, max_length=100)
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)

# response to client from api
class UserResponse(BaseModel):
    id: int
    full_name: str
    username: str
    email: str
    role: UserRole
    created_at: datetime

    class Config:
        from_attributes = True
