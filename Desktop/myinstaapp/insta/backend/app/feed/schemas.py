from pydantic import BaseModel
from datetime import datetime


class UserInfo(BaseModel):
    id: int
    username: str
    
    class Config:
        from_attributes = True


class PostInFeed(BaseModel):
    id: int
    user_id: int
    image_url: str
    caption: str
    created_at: datetime
    likes_count: int = 0
    comments_count: int = 0
    
    class Config:
        from_attributes = True


class FeedResponse(BaseModel):
    posts: list[PostInFeed]
    total: int
    skip: int
    limit: int
    
    class Config:
        from_attributes = True