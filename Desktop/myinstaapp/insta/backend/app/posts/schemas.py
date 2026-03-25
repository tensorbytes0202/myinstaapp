from pydantic import BaseModel
from datetime import datetime

class PostCreate(BaseModel):
    image_url: str
    caption: str


class PostResponse(BaseModel):
    id: int
    user_id: int
    image_url: str
    caption: str
    created_at: datetime
    likes_count: int = 0
    comments_count: int = 0
    
    class Config:
        from_attributes = True


class PostDetailResponse(BaseModel):
    id: int
    user_id: int
    image_url: str
    caption: str
    created_at: datetime
    likes_count: int
    comments_count: int
    
    class Config:
        from_attributes = True