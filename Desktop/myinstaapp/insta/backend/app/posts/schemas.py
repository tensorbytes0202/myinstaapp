from pydantic import BaseModel

class PostCreate(BaseModel):
    image_url: str
    caption: str


class PostResponse(BaseModel):

    id: int
    user_id: int
    image_url: str
    caption: str

    class Config:
        from_attributes = True