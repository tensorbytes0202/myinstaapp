from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.sql import func
from app.db.base import Base

class Comment(Base):
    
    __tablename__ = "comments"
    
    id = Column(Integer, primary_key=True, index=True)
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    
    text = Column(Text, nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())