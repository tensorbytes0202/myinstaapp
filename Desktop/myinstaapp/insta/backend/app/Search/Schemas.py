from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class UserSearchResult(BaseModel):
    id: int
    username: str
    
    class Config:
        from_attributes = True


class PostSearchResult(BaseModel):
    id: int
    user_id: int
    image_url: str
    caption: str
    created_at: datetime
    likes_count: int = 0
    comments_count: int = 0
    
    class Config:
        from_attributes = True


class SearchResponse(BaseModel):
    users: List[UserSearchResult]
    posts: List[PostSearchResult]
    query: str
    
    class Config:
        from_attributes = True


class UserSearchResponse(BaseModel):
    results: List[UserSearchResult]
    query: str
    total: int
    
    class Config:
        from_attributes = True


class PostSearchResponse(BaseModel):
    results: List[PostSearchResult]
    query: str
    total: int
    
    class Config:
        from_attributes = True


class HashtagSearchResponse(BaseModel):
    results: List[PostSearchResult]
    hashtag: str
    total: int
    
    class Config:
        from_attributes = True