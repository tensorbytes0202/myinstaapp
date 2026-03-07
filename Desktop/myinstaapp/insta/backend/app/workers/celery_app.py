from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "insta",
    broker=settings.RABBITMQ_URL,
    backend=settings.REDIS_URL
)