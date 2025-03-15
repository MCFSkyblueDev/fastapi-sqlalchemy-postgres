from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.config.database import Base
from app.models import user_group

class UserModel(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    
    items = relationship("ItemModel", back_populates="owner")
    profile = relationship("UserProfileModel", back_populates="user", uselist=False)
    user_groups = relationship("UserGroupModel", back_populates="user")

class UserProfileModel(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    bio = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)  # ForeignKey with unique=True

    user = relationship("UserModel", back_populates="profile")