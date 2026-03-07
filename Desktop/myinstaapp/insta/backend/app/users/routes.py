from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.deps import get_db
from app.users.schemas import UserCreate, UserResponse, UserLogin
from app.users.service import register_user, authenticate_user
from app.core.security import create_access_token

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/signup", response_model=UserResponse)
async def signup(user: UserCreate, db: AsyncSession = Depends(get_db)):

    new_user = await register_user(
        db,
        user.username,
        user.password
    )

    return new_user


@router.post("/login")
async def login(user: UserLogin, db: AsyncSession = Depends(get_db)):

    db_user = await authenticate_user(
        db,
        user.username,
        user.password
    )

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": db_user.username})

    return {"access_token": token}