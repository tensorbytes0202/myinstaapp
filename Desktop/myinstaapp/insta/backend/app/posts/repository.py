from sqlalchemy.ext.asyncio import AsyncSession
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