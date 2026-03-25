from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.follow.models import Follow
from sqlalchemy import func


async def create_follow(db: AsyncSession, follower_id: int, following_id: int):
    """Create follow relationship"""
    follow = Follow(
        follower_id=follower_id,
        following_id=following_id
    )
    db.add(follow)
    await db.commit()
    await db.refresh(follow)
    return follow


async def get_follow(db: AsyncSession, follower_id: int, following_id: int):
    """Check if user already follows another user"""
    result = await db.execute(
        select(Follow).where(
            (Follow.follower_id == follower_id) & 
            (Follow.following_id == following_id)
        )
    )
    return result.scalar_one_or_none()


async def get_follower_count(db: AsyncSession, user_id: int):
    """Get number of followers for a user"""
    result = await db.execute(
        select(func.count(Follow.id)).where(Follow.following_id == user_id)
    )
    return result.scalar() or 0


async def get_following_count(db: AsyncSession, user_id: int):
    """Get number of users this user is following"""
    result = await db.execute(
        select(func.count(Follow.id)).where(Follow.follower_id == user_id)
    )
    return result.scalar() or 0


async def get_followers(db: AsyncSession, user_id: int):
    """Get list of followers for a user"""
    result = await db.execute(
        select(Follow).where(Follow.following_id == user_id)
    )
    return result.scalars().all()


async def get_following(db: AsyncSession, user_id: int):
    """Get list of users this user is following"""
    result = await db.execute(
        select(Follow).where(Follow.follower_id == user_id)
    )
    return result.scalars().all()