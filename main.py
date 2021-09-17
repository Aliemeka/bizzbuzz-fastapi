from fastapi import FastAPI
from fastapi.routing import APIRouter
from typing import List

from core.routers import auth, posts
from core.config.database import engine
from core.models import postModel, userModel

userModel.BaseModel.metadata.create_all(bind=engine)
postModel.BaseModel.metadata.create_all(bind=engine)

app = FastAPI(
    title="Bizzbuzz API",
    version="1.0.0",
    description="Bizzbuzz api for post sharing social network",
)


def configure_routes(routers: List[APIRouter], prefix: str = "/api/v1"):
    for router in routers:
        app.include_router(router, prefix=prefix)


configure_routes([posts.router, auth.router])


@app.get("/")
def hello():
    return {"message": "Hello!, Welcome to Bizzbuzz on FastAPI"}
