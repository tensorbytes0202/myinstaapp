from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.deps import get_db
from app.search.schemas import (
    UserSearchResponse,
    PostSearchResponse,
    HashtagSearchResponse,
    SearchResponse
)
from app.search.service import (
    find_users,
    find_posts,
    find_hashtag,
    search_all
)

router = APIRouter(prefix="/search", tags=["search"])


# Search users
@router.get("/users", response_model=UserSearchResponse)
async def search_users_endpoint(
    q: str = Query(..., min_length=2, description="Search query"),
    limit: int = Query(10, ge=1, le=50),
    db: AsyncSession = Depends(get_db)
):
    """
    Search for users by username
    
    Query Parameters:
    - q: Search query (minimum 2 characters)
    - limit: Maximum results (1-50, default 10)
    
    Example: /search/users?q=aditya&limit=10
    """
    
    result = await find_users(db, q, limit)
    
    return result


# Search posts
@router.get("/posts", response_model=PostSearchResponse)
async def search_posts_endpoint(
    q: str = Query(..., min_length=2, description="Search query"),
    limit: int = Query(10, ge=1, le=50),
    db: AsyncSession = Depends(get_db)
):
    """
    Search for posts by caption content
    
    Query Parameters:
    - q: Search query (minimum 2 characters)
    - limit: Maximum results (1-50, default 10)
    
    Example: /search/posts?q=travel&limit=10
    """
    
    result = await find_posts(db, q, limit)
    
    return result


# Search hashtags
@router.get("/hashtags", response_model=HashtagSearchResponse)
async def search_hashtags_endpoint(
    tag: str = Query(..., min_length=2, description="Hashtag to search (with or without #)"),
    limit: int = Query(10, ge=1, le=50),
    db: AsyncSession = Depends(get_db)
):
    """
    Search for posts by hashtag
    
    Query Parameters:
    - tag: Hashtag (with or without #)
    - limit: Maximum results (1-50, default 10)
    
    Examples:
    - /search/hashtags?tag=travel
    - /search/hashtags?tag=%23travel (URL encoded #)
    """
    
    result = await find_hashtag(db, tag, limit)
    
    return result


# Global search (users + posts)
@router.get("/", response_model=SearchResponse)
async def global_search_endpoint(
    q: str = Query(..., min_length=2, description="Search query"),
    limit: int = Query(5, ge=1, le=10),
    db: AsyncSession = Depends(get_db)
):
    """
    Global search - search both users and posts
    
    Query Parameters:
    - q: Search query (minimum 2 characters)
    - limit: Maximum results per type (1-10, default 5)
    
    Returns:
    - users: List of matching users
    - posts: List of matching posts
    
    Example: /search/?q=travel&limit=5
    """
    
    result = await search_all(db, q, limit)
    
    return result