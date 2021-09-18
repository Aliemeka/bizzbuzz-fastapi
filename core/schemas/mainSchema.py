from datetime import datetime
from typing import List

from .postSchema import Post
from .userSchema import User


class PostDetails(Post):
    author: User

class UserDetails(User):
    posts: List[Post]
    created_at: datetime
    updated_at: datetime