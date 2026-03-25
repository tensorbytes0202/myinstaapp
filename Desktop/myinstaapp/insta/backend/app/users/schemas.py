from pydantic import BaseModel
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True


class PostInProfile(BaseModel):
    id: int
    image_url: str
    caption: str
    created_at: datetime
    likes_count: int = 0
    comments_count: int = 0
    
    class Config:
        from_attributes = True


class UserProfileResponse(BaseModel):
    id: int
    username: str
    followers_count: int
    following_count: int
    posts_count: int
    posts: list[PostInProfile] = []

    class Config:
        from_attributes = True