from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from app.likes.models import Like
from sqlalchemy import func

# Create a like
async def create_like(db: AsyncSession, user_id: int, post_id: int):
    
    like = Like(
        user_id=user_id,
        post_id=post_id
    )
    
    db.add(like)
    await db.commit()
    await db.refresh(like)
    
    return like


# Check if user has already liked the post
async def get_like(db: AsyncSession, user_id: int, post_id: int):
    
    result = await db.execute(
        select(Like).where(
            (Like.user_id == user_id) & (Like.post_id == post_id)
        )
    )
    
    return result.scalar_one_or_none()


# Delete a like (unlike)
async def delete_like(db: AsyncSession, user_id: int, post_id: int):
    
    await db.execute(
        delete(Like).where(
            (Like.user_id == user_id) & (Like.post_id == post_id)
        )
    )
    
    await db.commit()


# Get like count for a post
async def get_like_count(db: AsyncSession, post_id: int):
    
    result = await db.execute(
        select(func.count(Like.id)).where(Like.post_id == post_id)
    )
    
    return result.scalar() or 0


# Get all likes for a post
async def get_post_likes(db: AsyncSession, post_id: int):
    
    result = await db.execute(
        select(Like).where(Like.post_id == post_id).order_by(Like.created_at.desc())
    )
    
    return result.scalars().all()