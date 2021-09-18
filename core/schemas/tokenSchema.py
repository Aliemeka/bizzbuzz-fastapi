from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class Token(BaseModel):
    token: str
    user: str
    expires: datetime
    token_type: Optional[str] = "Bearer Token"
    is_active: bool
