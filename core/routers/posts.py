from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional, TypedDict
from sqlalchemy.orm.session import Session

from ..schemas.postSchema import Post, BasePost, Status
from ..repository import postRepo
from ..config.session import get_db

router = APIRouter(prefix="/posts", tags=["posts"])

StatusPayload = TypedDict("StatusPayload", status=Status)


@router.get("/", response_model=List[Post])
async def get_posts(
    status: Optional[Status] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
):
    posts = await postRepo.get_posts(db)
    if status != None:
        posts = postRepo.get_post_by_status(status, posts)
    if search:
        posts = postRepo.get_post_by_attribute(search, posts)
    return posts


@router.post("/", status_code=201, response_model=Post)
async def create_post(post: BasePost, db: Session = Depends(get_db)):
    return await postRepo.create_post(db, post)


@router.post("/multiple", status_code=201, response_model=List[Post])
async def add_multiple(posts: List[BasePost], db: Session = Depends(get_db)):
    return await postRepo.add_mulitple(db, posts)


@router.get("/{id}", response_model=Post)
async def get_post(id: int, db: Session = Depends(get_db)):
    try:
        post = await postRepo.get_post(db, id)
        return post
    except Exception as e:
        raise HTTPException(status_code=404, detail=e.args[0]["message"])


@router.put("/{id}", response_model=Post)
async def update_post(id: int, details: BasePost, db: Session = Depends(get_db)):
    try:
        post = await postRepo.edit_post(db, id, details)
        return post
    except Exception as e:
        raise HTTPException(status_code=404, detail=e.args[0]["message"])


@router.patch("/{id}/status", response_model=Post)
async def change_post_status(
    id: int, payload: StatusPayload, db: Session = Depends(get_db)
):
    try:
        post = await postRepo.change_post_status(db, id, payload["status"])
        return post
    except Exception as e:
        raise HTTPException(status_code=404, detail=e.args[0]["message"])


@router.delete("/{id}", response_model=TypedDict("Message", message=str))
async def remove_post(id: int, db: Session = Depends(get_db)):
    try:
        await postRepo.delete_post(db, id)
        return {"message": f"Post with id: {id} has been deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=404, detail=e.args[0]["message"])
