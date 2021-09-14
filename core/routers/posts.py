from fastapi import APIRouter, HTTPException
from typing import List, Optional, TypedDict
from ..schemas.postSchema import Post, BasePost, Status
from ..repository import postRepo

router = APIRouter(prefix="/posts", tags=["posts"])

StatusPayload = TypedDict("StatusPayload", status=Status)


@router.get("/", response_model=List[Post])
async def get_posts(status: Optional[Status] = None, search: Optional[str] = None):
    posts = postRepo.get_posts()
    if status != None:
        posts = postRepo.get_post_by_status(status, posts)
    if search:
        posts = postRepo.get_post_by_attribute(search, posts)
    return posts


@router.post("/", status_code=201, response_model=Post)
async def create_post(post: BasePost):
    return postRepo.create_post(post)


@router.post("/multiple", response_model=List[Post])
async def add_multiple(posts: List[BasePost]):
    return postRepo.add_mulitple(posts)


@router.get("/{id}", response_model=Post)
async def get_post(id: int):
    try:
        post = postRepo.get_post(id)
        return post
    except Exception as e:
        raise HTTPException(status_code=404, detail=e.args[0]["message"])


@router.put("/{id}", response_model=Post)
async def update_post(id: int, details: BasePost):
    try:
        post = postRepo.edit_post(id, details)
        return post
    except Exception as e:
        raise HTTPException(status_code=404, detail=e.args[0]["message"])


@router.patch("/{id}/status", response_model=Post)
async def change_post_status(id: int, payload: StatusPayload):
    try:
        post = postRepo.change_post_status(id, payload["status"])
        return post
    except Exception as e:
        raise HTTPException(status_code=404, detail=e.args[0]["message"])
