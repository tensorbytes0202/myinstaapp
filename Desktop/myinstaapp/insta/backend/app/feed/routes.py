from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.deps import get_db
from app.feed.schemas import FeedResponse
from app.feed.service import get_personalized_feed, get_explore, get_trending

router = APIRouter(prefix="/feed", tags=["feed"])


# Get personalized feed (posts from followed users)
@router.get("/", response_model=FeedResponse)
async def get_feed(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=50),
    db: AsyncSession = Depends(get_db)
):
    """
    Get personalized feed for current user
    - Shows posts from users that you follow
    - Ordered by newest first
    - Supports pagination with skip and limit
    
    Example: /feed/?skip=0&limit=10
    """
    
    # In real app, get current user from JWT token
    user_id = 1
    
    feed = await get_personalized_feed(db, user_id, skip, limit)
    
    return feed


# Get explore feed (all posts)
@router.get("/explore", response_model=FeedResponse)
async def explore(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=50),
    db: AsyncSession = Depends(get_db)
):
    """
    Get explore/discover feed
    - Shows all posts from all users
    - Ordered by newest first
    - Good for discovering new content
    """
    
    feed = await get_explore(db, skip, limit)
    
    return feed


# Get trending feed (most liked posts)
@router.get("/trending", response_model=FeedResponse)
async def trending(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=50),
    db: AsyncSession = Depends(get_db)
):
    """
    Get trending feed
    - Shows most liked posts first
    - Ordered by likes count (descending)
    - Good for discovering viral content
    """
    
    feed = await get_trending(db, skip, limit)
    
    return feed