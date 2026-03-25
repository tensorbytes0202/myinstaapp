from sqlalchemy.ext.asyncio import AsyncSession
from app.posts.repository import create_post
from app.likes.repository import get_like_count
from app.comments.repository import get_comment_count


async def create_new_post(db: AsyncSession, user_id: int, image_url: str, caption: str):
    
    post = await create_post(db, user_id, image_url, caption)
    
    # Add counts to response
    post.likes_count = 0
    post.comments_count = 0
    
    return post


async def get_post_with_counts(db: AsyncSession, post):
    """Add likes and comments count to post object"""
    
    likes_count = await get_like_count(db, post.id)
    comments_count = await get_comment_count(db, post.id)
    
    # Add as attributes
    post.likes_count = likes_count
    post.comments_count = comments_count
    
    return post