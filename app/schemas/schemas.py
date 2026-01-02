from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from app.models.models import UserRole

# --- PROJETS ---
class ProjectBase(BaseModel):
    title: str
    description: Optional[str] = None
    image_url: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectOut(ProjectBase):
    id: int
    user_id: int
    created_at: datetime
    class Config: from_attributes = True

# --- UTILISATEURS ---
class UserBase(BaseModel):
    username: str
    email: EmailStr
    role: UserRole
    city: str
    phone: Optional[str] = None

class UserCreate(UserBase):
    password: str
    specialty: Optional[str] = None
    shop_name: Optional[str] = None

class UserUpdate(BaseModel): # Dédié à la mise à jour profil
    bio: Optional[str] = None
    cv_url: Optional[str] = None
    phone: Optional[str] = None
    city: Optional[str] = None

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
    bio: Optional[str]
    cv_url: Optional[str]
    is_admin: bool
    is_active: bool
    projects: List[ProjectOut] = []
    class Config: from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    username: str
    role: str
    user_id: int
    is_admin: bool

# --- MESSAGERIE ---
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