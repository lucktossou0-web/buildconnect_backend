from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from app.models.models import UserRole

class UserBase(BaseModel):
    username: str
    email: EmailStr
    role: UserRole
    city: str

class UserCreate(UserBase):
    password: str
    specialty: Optional[str] = None
    shop_name: Optional[str] = None

class UserLogin(BaseModel):
    username: str
    password: str

class UserOut(UserBase):
    id: int
    avatar_url: str
    rating: float
    specialty: Optional[str]
    shop_name: Optional[str]
    category: Optional[str]
    description: Optional[str]
    class Config: from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    username: str
    role: str

class MessageCreate(BaseModel):
    receiver_id: int
    content: str

class MessageOut(BaseModel):
    id: int
    sender_id: int
    receiver_id: int
    content: str
    created_at: datetime
    class Config: from_attributes = True