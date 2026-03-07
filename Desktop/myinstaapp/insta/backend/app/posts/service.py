from sqlalchemy.ext.asyncio import AsyncSession
from app.posts.repository import create_post


async def create_new_post(db: AsyncSession, user_id: int, image_url: str, caption: str):

    return await create_post(
        db,
        user_id,
        image_url,
        caption
    )