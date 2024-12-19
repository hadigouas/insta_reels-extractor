from typing import Union

from pydantic import BaseModel, HttpUrl


class ReelResponse(BaseModel):
    id: str
    user_id: int
    thumbnail_url: Union[str, HttpUrl]  
    video_url: Union[str, HttpUrl]      
    caption: str
    like_count: int
    view_count: int