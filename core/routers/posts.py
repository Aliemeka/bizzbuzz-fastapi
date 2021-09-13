from fastapi import APIRouter
from typing import List
from ..schemas.postSchema import Post, BasePost
from ..repository import postRepo

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("/", response_model=List[Post])
async def get_posts():
    return postRepo.get_posts()


@router.post("/", status_code=201, response_model=Post)
async def create_post(post: BasePost):
    return postRepo.create_post(post)


@router.post("/multiple", response_model=List[Post])
async def add_multiple(posts: List[BasePost]):
    return postRepo.add_mulitple(posts)
