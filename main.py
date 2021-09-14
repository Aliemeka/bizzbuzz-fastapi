from fastapi import FastAPI
from core.routers import posts
from core.config.database import engine
from core.models import postModel

postModel.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Bizzbuzz API")

app.include_router(posts.router)


@app.get("/")
def hello():
    return {"message": "Hello!, Welcome to Bizzbuzz on fastAPI"}
