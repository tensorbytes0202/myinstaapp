from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from app.comments.models import Comment
from sqlalchemy import func

async def create_comment(db: AsyncSession, user_id: int, post_id: int, text: str):
    comment = Comment(user_id=user_id, post_id=post_id, text=text)
    db.add(comment)
    await db.commit()
    await db.refresh(comment)
    return comment

async def get_comment(db: AsyncSession, comment_id: int):
    result = await db.execute(
        select(Comment).where(Comment.id == comment_id)
    )
    return result.scalar_one_or_none()

async def get_post_comments(db: AsyncSession, post_id: int):
    result = await db.execute(
        select(Comment).where(Comment.post_id == post_id).order_by(Comment.created_at.desc())
    )
    return result.scalars().all()

async def get_comment_count(db: AsyncSession, post_id: int):
    result = await db.execute(
        select(func.count(Comment.id)).where(Comment.post_id == post_id)
    )
    return result.scalar() or 0

async def update_comment(db: AsyncSession, comment_id: int, text: str):
    comment = await get_comment(db, comment_id)
    if comment:
        comment.text = text
        await db.commit()
        await db.refresh(comment)
    return comment

async def delete_comment(db: AsyncSession, comment_id: int):
    await db.execute(
        delete(Comment).where(Comment.id == comment_id)
    )
    await db.commit()