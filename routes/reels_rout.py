import os
from typing import List

import dotenv
from fastapi import APIRouter, HTTPException
from instagrapi import Client
from pydantic import BaseModel

from pydantic_schema.login_model import LoginRequest
from pydantic_schema.reel_model import ReelResponse

dotenv.load_dotenv()

router = APIRouter()



def get_instagram_client(username: str, password: str):

    try:
        client = Client()
        client.login(username, password)
        return client
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Instagram login failed: {str(e)}"
        )
        
#test the login
@router.post("/login")
async def login(login_request: LoginRequest):

    try:
        client = get_instagram_client(
            login_request.username,
            login_request.password
        )
        return {"message": "Successfully logged in"}
    except HTTPException as e:
        raise e
    
    
@router.get("/reels", response_model=List[ReelResponse])
async def get_last_reels(username: str):

    try:
        client = get_instagram_client(
            os.getenv('INSTAGRAM_USERNAME'),
            os.getenv('INSTAGRAM_PASSWORD')
        )

       
        user_id = client.user_id_from_username(username)
        
        
        medias = client.user_medias(user_id, amount=20)  
        
    
        reels = [media for media in medias if media.media_type == 2 and hasattr(media, 'video_url')][:3]
        
        
        reel_responses = []
        for reel in reels:
            reel_responses.append(ReelResponse(
                id=str(reel.id),
                user_id=reel.user.pk,
                thumbnail_url=str(reel.thumbnail_url),  
                video_url=str(reel.video_url),         
                caption=reel.caption_text if reel.caption_text else "",
                like_count=reel.like_count,
                view_count=getattr(reel, 'view_count', 0)
            ))

        return reel_responses

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching Reels: {str(e)}")

