from pydantic import BaseModel

class FollowCreate(BaseModel):
    following_id: int


class FollowResponse(BaseModel):

    id: int
    follower_id: int
    following_id: int

    class Config:
        from_attributes = True