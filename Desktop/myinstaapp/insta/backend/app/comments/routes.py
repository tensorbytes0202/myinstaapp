from fastapi import APIRouter, Depends
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

router = APIRouter(prefix="/comments", tags=["comments"])

@router.post("/", response_model=CommentResponse)
async def create_comment(data: CommentCreate, db: AsyncSession = Depends(get_db)):
    user_id = 1
    comment = await create_post_comment(db, user_id, data.post_id, data.text)
    return comment

@router.get("/{post_id}", response_model=list[CommentResponse])
async def get_comments(post_id: int, db: AsyncSession = Depends(get_db)):
    comments = await get_post_all_comments(db, post_id)
    return comments

@router.get("/count/{post_id}", response_model=CommentCount)
async def get_comment_count(post_id: int, db: AsyncSession = Depends(get_db)):
    comment_count = await get_post_comment_count(db, post_id)
    return {"post_id": post_id, "comment_count": comment_count}

@router.put("/{comment_id}", response_model=CommentResponse)
async def update_comment(comment_id: int, data: CommentUpdate, db: AsyncSession = Depends(get_db)):
    user_id = 1
    comment = await update_post_comment(db, comment_id, user_id, data.text)
    return comment

@router.delete("/{comment_id}")
async def delete_comment(comment_id: int, db: AsyncSession = Depends(get_db)):
    user_id = 1
    await delete_post_comment(db, comment_id, user_id)
    return {"message": "Comment deleted successfully"}