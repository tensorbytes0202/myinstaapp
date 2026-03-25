from fastapi import APIRouter
from app.api.health import router as health_router
from app.users.routes import router as users_router
from app.posts.routes import router as posts_router
from app.follow.routes import router as follow_router
from app.likes.routes import router as likes_router
from app.comments.routes import router as comments_router

api_router = APIRouter()

api_router.include_router(health_router)
api_router.include_router(users_router)
api_router.include_router(posts_router)
api_router.include_router(follow_router)
api_router.include_router(likes_router)
api_router.include_router(comments_router)
