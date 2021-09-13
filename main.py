from fastapi import FastAPI
from core.routers import posts

app = FastAPI(title="Bizzbuzz API")

app.include_router(posts.router)


@app.get("/")
def hello():
    return {"message": "Hello!, Welcome to Bizzbuzz on fastAPI"}
