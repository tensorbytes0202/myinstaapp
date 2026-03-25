from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.search.repository import (
    search_users,
    search_posts,
    search_hashtags,
    global_search
)
from app.likes.repository import get_like_count
from app.comments.repository import get_comment_count


async def find_users(db: AsyncSession, query: str, limit: int = 10):
    """
    Search for users
    """
    
    if not query or len(query.strip()) < 2:
        raise HTTPException(
            status_code=400,
            detail="Search query must be at least 2 characters"
        )
    
    users = await search_users(db, query, limit)
    
    return {
        "results": users,
        "query": query,
        "total": len(users)
    }


async def find_posts(db: AsyncSession, query: str, limit: int = 10):
    """
    Search for posts by caption
    """
    
    if not query or len(query.strip()) < 2:
        raise HTTPException(
            status_code=400,
            detail="Search query must be at least 2 characters"
        )
    
    posts = await search_posts(db, query, limit)
    
    # Add likes and comments count
    for post in posts:
        post.likes_count = await get_like_count(db, post.id)
        post.comments_count = await get_comment_count(db, post.id)
    
    return {
        "results": posts,
        "query": query,
        "total": len(posts)
    }


async def find_hashtag(db: AsyncSession, hashtag: str, limit: int = 10):
    """
    Search for posts by hashtag
    """
    
    if not hashtag or len(hashtag.strip()) < 2:
        raise HTTPException(
            status_code=400,
            detail="Hashtag must be at least 2 characters"
        )
    
    posts = await search_hashtags(db, hashtag, limit)
    
    # Add likes and comments count
    for post in posts:
        post.likes_count = await get_like_count(db, post.id)
        post.comments_count = await get_comment_count(db, post.id)
    
    return {
        "results": posts,
        "hashtag": hashtag,
        "total": len(posts)
    }


async def search_all(db: AsyncSession, query: str, limit: int = 5):
    """
    Global search - search users and posts together
    """
    
    if not query or len(query.strip()) < 2:
        raise HTTPException(
            status_code=400,
            detail="Search query must be at least 2 characters"
        )
    
    results = await global_search(db, query, limit)
    
    # Add counts to posts
    for post in results["posts"]:
        post.likes_count = await get_like_count(db, post.id)
        post.comments_count = await get_comment_count(db, post.id)
    
    return {
        "users": results["users"],
        "posts": results["posts"],
        "query": query
    }