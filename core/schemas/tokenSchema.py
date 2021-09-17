from pydantic import BaseModel
from typing import Optional


class Token(BaseModel):
    token: str
    user: str
    token_type: Optional[str] = "Bearer Token"
    is_active: bool
