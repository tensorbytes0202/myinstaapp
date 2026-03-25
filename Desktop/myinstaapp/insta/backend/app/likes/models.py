from sqlalchemy import Column, Integer, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.sql import func
from app.db.base import Base
 
class Like(Base):
    
    __tablename__ = "likes"
    
    id = Column(Integer, primary_key=True, index=True)
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Ensure one user can't like the same post multiple times
    __table_args__ = (UniqueConstraint('user_id', 'post_id', name='unique_user_post_like'),)
 