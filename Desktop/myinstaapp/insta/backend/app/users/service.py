from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.users.repository import get_user_by_username, create_user, get_user_by_id
from app.core.security import hash_password, verify_password
from app.follow.repository import get_follower_count, get_following_count
from app.posts.repository import get_user_posts
from app.likes.repository import get_like_count
from app.comments.repository import get_comment_count
from sqlalchemy import select, func
from app.posts.models import Post


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


async def get_user_profile(db: AsyncSession, user_id: int):
    """Get complete user profile with posts and counts"""
    
    user = await get_user_by_id(db, user_id)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get follower and following counts
    followers_count = await get_follower_count(db, user_id)
    following_count = await get_following_count(db, user_id)
    
    # Get all user posts
    posts = await get_user_posts(db, user_id)
    
    # Add likes and comments count to each post
    posts_with_counts = []
    for post in posts:
        likes_count = await get_like_count(db, post.id)
        comments_count = await get_comment_count(db, post.id)
        
        post.likes_count = likes_count
        post.comments_count = comments_count
        posts_with_counts.append(post)
    
    # Create response object
    profile = {
        "id": user.id,
        "username": user.username,
        "followers_count": followers_count,
        "following_count": following_count,
        "posts_count": len(posts_with_counts),
        "posts": posts_with_counts
    }
    
    return profile


async def get_user_profile_by_username(db: AsyncSession, username: str):
    """Get user profile by username"""
    
    user = await get_user_by_username(db, username)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return await get_user_profile(db, user.id)