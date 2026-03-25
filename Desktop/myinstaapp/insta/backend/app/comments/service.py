from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.comments.repository import (
    create_comment,
    get_comment,
    delete_comment,
    get_comment_count,
    get_post_comments,
    update_comment
)

async def create_post_comment(db: AsyncSession, user_id: int, post_id: int, text: str):
    if not text or len(text.strip()) == 0:
        raise HTTPException(status_code=400, detail="Comment text cannot be empty")
    
    if len(text) > 500:
        raise HTTPException(status_code=400, detail="Comment text cannot exceed 500 characters")
    
    comment = await create_comment(db, user_id, post_id, text)
    return comment

async def get_post_all_comments(db: AsyncSession, post_id: int):
    return await get_post_comments(db, post_id)

async def get_post_comment_count(db: AsyncSession, post_id: int):
    return await get_comment_count(db, post_id)

async def update_post_comment(db: AsyncSession, comment_id: int, user_id: int, text: str):
    comment = await get_comment(db, comment_id)
    
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    if comment.user_id != user_id:
        raise HTTPException(status_code=403, detail="You can only edit your own comments")
    
    if not text or len(text.strip()) == 0:
        raise HTTPException(status_code=400, detail="Comment text cannot be empty")
    
    if len(text) > 500:
        raise HTTPException(status_code=400, detail="Comment text cannot exceed 500 characters")
    
    updated_comment = await update_comment(db, comment_id, text)
    return updated_comment

async def delete_post_comment(db: AsyncSession, comment_id: int, user_id: int):
    comment = await get_comment(db, comment_id)
    
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    if comment.user_id != user_id:
        raise HTTPException(status_code=403, detail="You can only delete your own comments")
    
    await delete_comment(db, comment_id)