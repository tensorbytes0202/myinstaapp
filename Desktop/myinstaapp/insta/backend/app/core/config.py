from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    DATABASE_URL: str = "postgresql+asyncpg://insta:insta@localhost:5432/insta_db"

    REDIS_URL: str = "redis://localhost:6379/0"

    RABBITMQ_URL: str = "amqp://guest:guest@localhost:5672//"

    SECRET_KEY: str = "supersecretkey"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15

settings = Settings()