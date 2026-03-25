import asyncio
from app.db.session import engine
from app.db.base import Base

# import all models
from app.users.models import User
from app.posts.models import Post
from app.follow.models import Follow
from app.likes.models import Like
from app.comments.models import Comment  # ✅ Add this
from app.notifications.models import Notification


async def create_tables():

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


asyncio.run(create_tables())