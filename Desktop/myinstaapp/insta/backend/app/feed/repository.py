from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.posts.models import Post
from app.follow.models import Follow


async def get_user_feed(db: AsyncSession, user_id: int, skip: int = 0, limit: int = 10):
    """
    Get feed posts for a user
    - Shows posts from users that the current user follows
    - Ordered by newest first
    - With pagination (skip, limit)
    """
    
    # Get all users that current user follows
    following_result = await db.execute(
        select(Follow.following_id).where(Follow.follower_id == user_id)
    )
    
    following_ids = following_result.scalars().all()
    
    # If user doesn't follow anyone, return empty list
    if not following_ids:
        return []
    
    # Get posts from followed users
    posts_result = await db.execute(
        select(Post)
        .where(Post.user_id.in_(following_ids))
        .order_by(Post.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    
    posts = posts_result.scalars().all()
    
    return posts


async def get_explore_feed(db: AsyncSession, skip: int = 0, limit: int = 10):
    """
    Get explore/discover feed
    - Shows all posts from all users
    - Ordered by newest first
    - Good for discovery
    """
    
    result = await db.execute(
        select(Post)
        .order_by(Post.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    
    return result.scalars().all()


async def get_trending_feed(db: AsyncSession, skip: int = 0, limit: int = 10):
    """
    Get trending feed
    - Shows posts sorted by likes count (most liked first)
    - Good for discovering viral content
    """
    
    from sqlalchemy import func, desc
    from app.likes.models import Like
    
    result = await db.execute(
        select(Post)
        .outerjoin(Like)
        .group_by(Post.id)
        .order_by(desc(func.count(Like.id)))
        .offset(skip)
        .limit(limit)
    )
    
    return result.scalars().all()