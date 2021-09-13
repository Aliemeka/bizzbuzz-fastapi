from typing import List

from ..schemas.postSchema import BasePost, Post


posts: List[Post] = []


def get_posts():
    return posts


def create_post(post: BasePost):
    somePost = dict(post)
    somePost["id"] = len(posts) + 1
    newPost = Post(**somePost)
    posts.append(newPost)
    return newPost


def add_posts(posts: List[BasePost]):
    for post in posts:
        yield create_post(post)


def add_mulitple(postList: List[BasePost]):
    posts = [post for post in add_posts(postList)]
    print(posts)
    return posts
