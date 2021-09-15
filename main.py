from fastapi import FastAPI
from core.routers import posts
from core.config.database import engine
from core.models import postModel

postModel.BaseModel.metadata.create_all(bind=engine)

app = FastAPI(
    title="Bizzbuzz API",
    version="1.0.0",
    description="Bizzbuzz api for post sharing social network",
)

app.include_router(posts.router, prefix="/api/v1")


@app.get("/")
def hello():
    return {"message": "Hello!, Welcome to Bizzbuzz on fastAPI"}
