from pydantic import BaseModel
from datetime import datetime

class CommentCreate(BaseModel):
    post_id: int
    text: str


class CommentUpdate(BaseModel):
    text: str


class CommentResponse(BaseModel):
    id: int
    user_id: int
    post_id: int
    text: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class CommentCount(BaseModel):
    post_id: int
    comment_count: int