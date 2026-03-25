from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, ilike
from app.users.models import User
from app.posts.models import Post


async def search_users(db: AsyncSession, query: str, limit: int = 10):
    """
    Search users by username
    Case-insensitive search
    """
    
    if not query or len(query.strip()) < 2:
        return []
    
    search_query = f"%{query}%"
    
    result = await db.execute(
        select(User)
        .where(User.username.ilike(search_query))
        .limit(limit)
    )
    
    return result.scalars().all()


async def search_posts(db: AsyncSession, query: str, limit: int = 10):
    """
    Search posts by caption
    Case-insensitive search
    """
    
    if not query or len(query.strip()) < 2:
        return []
    
    search_query = f"%{query}%"
    
    result = await db.execute(
        select(Post)
        .where(Post.caption.ilike(search_query))
        .order_by(Post.created_at.desc())
        .limit(limit)
    )
    
    return result.scalars().all()


async def search_hashtags(db: AsyncSession, hashtag: str, limit: int = 10):
    """
    Search posts by hashtag in caption
    Example: search for #travel returns all posts with #travel
    """
    
    if not hashtag:
        return []
    
    # Add # if not present
    if not hashtag.startswith("#"):
        hashtag = f"#{hashtag}"
    
    search_query = f"%{hashtag}%"
    
    result = await db.execute(
        select(Post)
        .where(Post.caption.ilike(search_query))
        .order_by(Post.created_at.desc())
        .limit(limit)
    )
    
    return result.scalars().all()


async def global_search(db: AsyncSession, query: str, limit: int = 5):
    """
    Global search - search both users and posts
    Returns both users and posts matching the query
    """
    
    if not query or len(query.strip()) < 2:
        return {"users": [], "posts": []}
    
    search_query = f"%{query}%"
    
    # Search users
    users_result = await db.execute(
        select(User)
        .where(User.username.ilike(search_query))
        .limit(limit)
    )
    users = users_result.scalars().all()
    
    # Search posts
    posts_result = await db.execute(
        select(Post)
        .where(Post.caption.ilike(search_query))
        .order_by(Post.created_at.desc())
        .limit(limit)
    )
    posts = posts_result.scalars().all()
    
    return {
        "users": users,
        "posts": posts
    }