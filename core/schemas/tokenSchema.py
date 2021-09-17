from pydantic import BaseModel


class Token(BaseModel):
    token: str
    user: str
    is_active: bool
