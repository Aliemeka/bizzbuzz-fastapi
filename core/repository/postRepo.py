from typing import List
from asyncio.runners import run
from sqlalchemy.orm import Session

from ..schemas.postSchema import BasePost, Post, Status
from ..models.postModel import PostModel


async def get_posts(db: Session):
    posts = [post for post in db.query(PostModel).all()]
    return posts


async def create_post(db: Session, post: BasePost):
    db_post = PostModel(**post.dict())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    print(db_post)
    return db_post


async def add_posts(db: Session, posts: List[BasePost]):
    for post in posts:
        yield await create_post(db, post)


async def add_mulitple(db: Session, postList: List[BasePost]):

    posts = [post async for post in add_posts(db, postList)]
    return posts


async def get_post(db: Session, id: str):
    posts = await get_posts(db)
    if len(posts) < 1:
        raise Exception({"message": "There are no posts yet!"})

    db_post = db.query(PostModel).filter(PostModel.id == id).first()
    if db_post:
        return db_post

    raise Exception({"message": f"Cannot find post with id: {id}"})


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


async def edit_post(db: Session, id: str, details: BasePost):
    post = await get_post(db, id)
    post.title = details.title
    post.description = details.description
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
