from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.deps import get_db
from app.follow.schemas import FollowCreate, FollowResponse
from app.follow.service import follow_user

router = APIRouter(prefix="/follow", tags=["follow"])


@router.post("/", response_model=FollowResponse)
async def follow(data: FollowCreate, db: AsyncSession = Depends(get_db)):

    follower_id = 1

    follow = await follow_user(
        db,
        follower_id,
        data.following_id
    )

    return follow