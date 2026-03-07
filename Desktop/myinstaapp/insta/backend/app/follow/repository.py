from sqlalchemy.ext.asyncio import AsyncSession
from app.follow.models import Follow


async def create_follow(db: AsyncSession, follower_id: int, following_id: int):

    follow = Follow(
        follower_id=follower_id,
        following_id=following_id
    )

    db.add(follow)

    await db.commit()

    await db.refresh(follow)

    return follow