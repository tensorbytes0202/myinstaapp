from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.users.models import User


async def get_user_by_username(db: AsyncSession, username: str):
    """Get user by username"""
    result = await db.execute(
        select(User).where(User.username == username)
    )
    return result.scalar_one_or_none()


async def get_user_by_id(db: AsyncSession, user_id: int):
    """Get user by ID"""
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    return result.scalar_one_or_none()


async def create_user(db: AsyncSession, username: str, password_hash: str):
    """Create new user"""
    user = User(
        username=username,
        password_hash=password_hash
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user