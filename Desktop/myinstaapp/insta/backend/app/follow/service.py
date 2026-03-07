from sqlalchemy.ext.asyncio import AsyncSession
from app.follow.repository import create_follow


async def follow_user(db: AsyncSession, follower_id: int, following_id: int):

    return await create_follow(
        db,
        follower_id,
        following_id
    )