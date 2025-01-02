from fastapi import FastAPI

from routes import reels_rout

app = FastAPI()


app.include_router(reels_rout.router, prefix="/insta")
