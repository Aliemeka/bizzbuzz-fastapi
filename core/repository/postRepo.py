from typing import List

from ..schemas.postSchema import BasePost, Post, Status


posts: List[Post] = []


def generate_number():
    i = 1
    while True:
        yield i
        i += 1


post_id = generate_number()


def get_posts():
    return posts


def create_post(post: BasePost):
    somePost = dict(post)
    somePost["id"] = next(post_id)
    newPost = Post(**somePost)
    posts.append(newPost)
    return newPost


def add_posts(posts: List[BasePost]):
    for post in posts:
        yield create_post(post)


def add_mulitple(postList: List[BasePost]):
    posts = [post for post in add_posts(postList)]
    return posts


def get_post(id: int):
    if len(posts) < 1:
        raise Exception({"message": "There are no posts yet!"})
    for post in posts:
        if post.id == id:
            return post

    raise Exception({"message": f"Cannot find post with id: {id}"})


def get_post_by_status(status: Status, postList: List[Post]):
    return [post for post in postList if post.status == status]


def get_post_by_attribute(attribute: str, postList: List[Post]):
    return [
        post
        for post in postList
        if attribute.lower() in post.name.lower()
        or attribute.lower() in post.description.lower()
    ]


def edit_post(id: int, details: BasePost):
    post = get_post(id)
    post.name = details.name
    post.description = details.description
    return post


def change_post_status(id: int, status: Status):
    post = get_post(id)
    post.status = status
    return post

def delete_post(id: int):
    post = get_post(id)
    del(post)