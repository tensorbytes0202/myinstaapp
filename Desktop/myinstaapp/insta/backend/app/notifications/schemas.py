from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class NotificationResponse(BaseModel):
    id: int
    recipient_id: int
    actor_id: int
    notification_type: str  # "like", "comment", "follow"
    post_id: Optional[int] = None
    comment_id: Optional[int] = None
    message: Optional[str] = None
    is_read: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class NotificationWithActor(BaseModel):
    id: int
    recipient_id: int
    actor_id: int
    actor_username: str
    notification_type: str
    post_id: Optional[int] = None
    comment_id: Optional[int] = None
    message: Optional[str] = None
    is_read: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class NotificationListResponse(BaseModel):
    notifications: list[NotificationWithActor]
    total: int
    unread_count: int
    
    class Config:
        from_attributes = True


class MarkNotificationAsRead(BaseModel):
    is_read: bool