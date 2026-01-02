from sqlalchemy import Column, Integer, String, Enum, ForeignKey, Text, DateTime, Float, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base
import enum

class UserRole(str, enum.Enum):
    CLIENT = "client"
    PRESTATAIRE = "prestataire"
    FOURNISSEUR = "fournisseur"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    city = Column(String, nullable=False)
    phone = Column(String, nullable=True) # Ajout téléphone

    # Statuts spéciaux
    is_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True) # False = Banni

    # Profil public
    specialty = Column(String, nullable=True)
    shop_name = Column(String, nullable=True)
    category = Column(String, nullable=True)
    avatar_url = Column(String, default="https://i.pravatar.cc/150")
    rating = Column(Float, default=4.5)
    description = Column(Text, nullable=True)
    bio = Column(Text, nullable=True)
    cv_url = Column(String, nullable=True)

    # Relations
    sent_messages = relationship("Message", foreign_keys="Message.sender_id", back_populates="sender")
    received_messages = relationship("Message", foreign_keys="Message.receiver_id", back_populates="receiver")
    projects = relationship("Project", back_populates="owner", cascade="all, delete-orphan")

class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    image_url = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    owner = relationship("User", back_populates="projects")

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("users.id"))
    receiver_id = Column(Integer, ForeignKey("users.id"))
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    sender = relationship("User", foreign_keys=[sender_id], back_populates="sent_messages")
    receiver = relationship("User", foreign_keys=[receiver_id], back_populates="received_messages")