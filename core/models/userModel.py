from sqlalchemy import String, Integer, Enum, Column


from .base import BaseModel
from ..config.enums import Status


class UserModel(BaseModel):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    status = Column(Enum(Status))
