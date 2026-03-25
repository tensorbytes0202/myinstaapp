from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.likes.repository import (
    create_like,
    get_like,
    delete_like,
    get_like_count,
    get_post_likes
)


# Like a post
async def like_post(db: AsyncSession, user_id: int, post_id: int):
    
    # Check if already liked
    existing_like = await get_like(db, user_id, post_id)
    
    if existing_like:
        raise HTTPException(
            status_code=400,
            detail="User has already liked this post"
        )
    
    like = await create_like(db, user_id, post_id)
    
    return like


# Unlike a post
async def unlike_post(db: AsyncSession, user_id: int, post_id: int):
    
    # Check if like exists
    existing_like = await get_like(db, user_id, post_id)
    
    if not existing_like:
        raise HTTPException(
            status_code=404,
            detail="Like not found"
        )
    
    await delete_like(db, user_id, post_id)


# Get like count for a post
async def get_post_like_count(db: AsyncSession, post_id: int):
    
    return await get_like_count(db, post_id)


# Get all people who liked a post
async def get_post_likers(db: AsyncSession, post_id: int):
    
    return await get_post_likes(db, post_id)