from sqlalchemy import Column, Integer, String, ForeignKey, true
from sqlalchemy.orm import relationship
from app.config.database import Base

class ItemModel(Base):
    __tablename__ = "items"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    image = Column(String, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    
    owner = relationship("UserModel", back_populates="items")
