from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.deps import get_db
from app.comments.schemas import CommentCreate, CommentResponse, CommentUpdate, CommentCount
from app.comments.service import (
    create_post_comment,
    get_post_all_comments,
    get_post_comment_count,
    update_post_comment,
    delete_post_comment
)
from app.notifications.service import notify_comment
from app.posts.repository import get_post

router = APIRouter(prefix="/comments", tags=["comments"])


# Create a comment on a post
@router.post("/", response_model=CommentResponse)
async def create_comment(data: CommentCreate, db: AsyncSession = Depends(get_db)):
    
    # In real app, get current user from JWT token
    user_id = 1
    
    # Get post to find owner
    post = await get_post(db, data.post_id)
    
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    comment = await create_post_comment(db, user_id, data.post_id, data.text)
    
    # Create notification for post owner
    if post.user_id != user_id:
        await notify_comment(db, post.user_id, user_id, data.post_id, comment.id)
    
    return comment


# Get all comments for a post
@router.get("/{post_id}", response_model=list[CommentResponse])
async def get_comments(post_id: int, db: AsyncSession = Depends(get_db)):
    
    comments = await get_post_all_comments(db, post_id)
    
    return comments


# Get comment count for a post
@router.get("/count/{post_id}", response_model=CommentCount)
async def get_comment_count(post_id: int, db: AsyncSession = Depends(get_db)):
    
    comment_count = await get_post_comment_count(db, post_id)
    
    return {
        "post_id": post_id,
        "comment_count": comment_count
    }


# Update a comment
@router.put("/{comment_id}", response_model=CommentResponse)
async def update_comment(comment_id: int, data: CommentUpdate, db: AsyncSession = Depends(get_db)):
    
    # In real app, get current user from JWT token
    user_id = 1
    
    comment = await update_post_comment(db, comment_id, user_id, data.text)
    
    return comment


# Delete a comment
@router.delete("/{comment_id}")
async def delete_comment(comment_id: int, db: AsyncSession = Depends(get_db)):
    
    # In real app, get current user from JWT token
    user_id = 1
    
    await delete_post_comment(db, comment_id, user_id)
    
    return {"message": "Comment deleted successfully"}