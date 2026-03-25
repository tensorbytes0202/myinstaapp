from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.posts.models import Post


async def create_post(db: AsyncSession, user_id: int, image_url: str, caption: str):
    
    post = Post(
        user_id=user_id,
        image_url=image_url,
        caption=caption
    )
    
    db.add(post)
    await db.commit()
    await db.refresh(post)
    
    return post


async def get_post(db: AsyncSession, post_id: int):
    """Get a single post by ID"""
    
    result = await db.execute(
        select(Post).where(Post.id == post_id)
    )
    
    return result.scalar_one_or_none()


async def get_user_posts(db: AsyncSession, user_id: int):
    """Get all posts by a user"""
    
    result = await db.execute(
        select(Post).where(Post.user_id == user_id).order_by(Post.created_at.desc())
    )
    
    return result.scalars().all()


async def get_all_posts(db: AsyncSession):
    """Get all posts"""
    
    result = await db.execute(
        select(Post).order_by(Post.created_at.desc())
    )
    
    return result.scalars().all()