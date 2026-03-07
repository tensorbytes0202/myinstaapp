from sqlalchemy.ext.asyncio import AsyncSession
from app.users.repository import get_user_by_username, create_user
from app.core.security import hash_password, verify_password

async def register_user(db: AsyncSession, username: str, password: str):

    password_hash = hash_password(password)

    return await create_user(
        db,
        username=username,
        password_hash=password_hash
    )


async def authenticate_user(db: AsyncSession, username: str, password: str):

    user = await get_user_by_username(db, username)

    if not user:
        return None

    if not verify_password(password, user.password_hash):
        return None

    return user