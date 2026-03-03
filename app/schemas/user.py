"""
User schemas — request/response validation for user endpoints.
"""

from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class UserCreate(BaseModel):
    """Schema for user registration."""
    name: str
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    """Schema for login."""
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    """Schema for updating user profile."""
    name: Optional[str] = None
    college: Optional[str] = None
    year: Optional[str] = None
    phone: Optional[str] = None
    bio: Optional[str] = None


class UserResponse(BaseModel):
    """Schema for user response (basic info)."""
    id: int
    name: str
    email: EmailStr

    class Config:
        from_attributes = True


class UserProfileResponse(BaseModel):
    """Schema for full user profile response."""
    id: int
    name: str
    email: EmailStr
    college: str
    year: str
    phone: str
    bio: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
