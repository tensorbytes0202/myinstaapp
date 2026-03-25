from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.sql import func
from app.db.base import Base

class Notification(Base):
    
    __tablename__ = "notifications"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # User who receives the notification
    recipient_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # User who triggered the notification
    actor_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Type of notification: like, comment, follow
    notification_type = Column(String, nullable=False)  # "like", "comment", "follow"
    
    # Reference to post (for like/comment notifications)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=True)
    
    # Reference to comment (for comment notifications)
    comment_id = Column(Integer, ForeignKey("comments.id"), nullable=True)
    
    # Message/content
    message = Column(String, nullable=True)
    
    # Whether notification is read
    is_read = Column(Boolean, default=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())