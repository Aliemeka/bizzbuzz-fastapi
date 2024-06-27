from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from typing_extensions import TypedDict
from sqlalchemy.orm.session import Session
from uuid import UUID

from ..schemas.postSchema import Post, PostCreate, Status
from ..schemas.userSchema import User
from ..schemas.mainSchema import PostDetails
from ..repository import postRepo
from ..repository.postRepo import NotFoundException, UnauthorizedOperationError
from ..config.session import get_db
from ..dependencies.validations import validate_id
from ..dependencies.authentication import JWTBearer

router = APIRouter(prefix="/posts", tags=["posts"])

StatusPayload = TypedDict("StatusPayload", status=Status)


@router.get("/", response_model=List[PostDetails])
async def get_posts(
    status: Optional[Status] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
):
    posts = await postRepo.get_posts(db)
    if len(posts):
        if status != None:
            posts = postRepo.get_post_by_status(status, posts)
        if search:
            posts = postRepo.get_post_by_attribute(search, posts)
    return posts


@router.post("/", status_code=201, response_model=Post)
async def create_post(
    post: PostCreate, db: Session = Depends(get_db), user: User = Depends(JWTBearer())
):
    return await postRepo.create_post(db, post, str(user.id))


@router.post("/multiple", status_code=201, response_model=List[Post])
async def add_multiple(
    posts: List[PostCreate],
    db: Session = Depends(get_db),
    user: User = Depends(JWTBearer()),
):
    return await postRepo.add_mulitple(db, posts, user.id)


@router.get("/{id}", response_model=Post)
async def get_post(id: str = Depends(validate_id), db: Session = Depends(get_db)):
    try:
        post = await postRepo.get_post(db, id)
        return post
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=e.args[0]["message"])


@router.put("/{id}", response_model=Post)
async def update_post(
    details: PostCreate,
    id: str = Depends(validate_id),
    db: Session = Depends(get_db),
    user: User = Depends(JWTBearer()),
):
    try:
        post = await postRepo.edit_post(db, id, details, user.id)
        return post
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=e.args[0]["message"])


@router.patch("/{id}/status", response_model=Post)
async def change_post_status(
    payload: StatusPayload,
    id: str = Depends(validate_id),
    db: Session = Depends(get_db),
    user: User = Depends(JWTBearer()),
):
    try:
        post = await postRepo.change_post_status(db, id, payload["status"], user.id)
        return post
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=e.args[0]["message"])
    except UnauthorizedOperationError as e:
        raise HTTPException(status_code=403, detail=e.args[0]["message"])


@router.delete("/{id}", response_model=TypedDict("Message", message=str))
async def remove_post(
    id: str = Depends(validate_id),
    db: Session = Depends(get_db),
    user: User = Depends(JWTBearer()),
):
    try:
        await postRepo.delete_post(db, id, user.id)
        return {"message": f"Post with id: {id} has been deleted successfully"}
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=e.args[0]["message"])
