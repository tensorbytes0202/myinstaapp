from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.users.models import User

async def get_user_by_username(db: AsyncSession, username: str):

    result = await db.execute(
        select(User).where(User.username == username)
    )

    return result.scalar_one_or_none()


async def create_user(db: AsyncSession, username: str, password_hash: str):

    user = User(
        username=username,
        password_hash=password_hash
    )

    db.add(user)

    await db.commit()

    await db.refresh(user)

    return user