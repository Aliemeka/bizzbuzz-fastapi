from core.repository.userRepo import get_user_by_id
from typing import List
from uuid import UUID
from sqlalchemy.orm import Session

from ..models.postModel import Post as PostModel
from ..schemas.postSchema import PostCreate, Post, Status


class NotFoundException(Exception):
    pass


class UnauthorizedOperationError(Exception):
    def __init__(self, message: str):
        super().__init__({"message": message})


async def get_posts(db: Session):
    posts = [post for post in db.query(PostModel).all()]
    for post in posts:
        post.author = await get_user_by_id(db, post.author_id)
    return posts


async def create_post(db: Session, post: PostCreate, user_id: str):
    db_post = PostModel(**post.dict(), author_id=user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


async def add_posts(db: Session, posts: List[PostCreate], user_id: str):
    for post in posts:
        yield await create_post(db, post, user_id)


async def add_mulitple(db: Session, postList: List[PostCreate], user_id: str):

    posts = [post async for post in add_posts(db, postList, user_id)]
    return posts


async def get_post(db: Session, id: str):
    posts = await get_posts(db)
    if len(posts) < 1:
        raise NotFoundException({"message": "There are no posts yet!"})

    db_post = db.query(PostModel).filter(PostModel.id == id).first()
    if db_post:
        return db_post

    raise NotFoundException({"message": f"Cannot find post with id: {id}"})


def get_post_by_status(status: Status, postList: List[Post]) -> List[Post]:
    """
    Returns post that match the status
    """
    return [post for post in postList if post.status == status]


def get_post_by_attribute(attribute: str, postList: List[Post]) -> List[Post]:
    """
    Returns post which name or descriptions contain the search string
    """
    return [
        post
        for post in postList
        if attribute.lower() in post.title.lower()
        or attribute.lower() in post.description.lower()
    ]


async def edit_post(db: Session, id: str, details: PostCreate, user_id: str):
    post = await get_post(db, id)
    if str(post.author_id) != str(user_id):
        raise UnauthorizedOperationError(
            "Only post author can carry out operation on this post"
        )
    post.title = details.title
    post.description = details.description
    if details.status:
        post.status = details.status
    db.commit()
    db.refresh(post)
    return post


async def change_post_status(db: Session, id: str, status: Status):
    post = await get_post(db, id)
    post.status = status
    db.commit()
    db.refresh(post)
    return post


async def delete_post(db: Session, id: str):
    post = await get_post(db, id)
    db.delete(post)
    db.commit()
