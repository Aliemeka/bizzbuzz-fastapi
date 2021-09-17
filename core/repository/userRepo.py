import re
from sqlalchemy.orm import Session

from ..schemas.userSchema import UserCreate
from ..models.userModel import User as UserModel
from ..utils.authentication import Hash


class UserAlreadyExistException(Exception):
    pass


async def email_exist(db: Session, email: str) -> bool:
    db_user = db.query(UserModel).filter(UserModel.email == email).one_or_none()
    if db_user == None:
        return False
    return True


async def username_exist(db: Session, username: str) -> bool:
    db_user = db.query(UserModel).filter(UserModel.username == username).one_or_none()
    if db_user == None:
        return False
    return True


async def create_user(db: Session, details: UserCreate):
    if await email_exist(db, details.email):
        raise UserAlreadyExistException(
            {"message": "Email already exist", "field": "email"}
        )
    if await username_exist(db, details.username):
        raise UserAlreadyExistException(
            {"message": "Username already exist", "field": "username"}
        )

    db_user = UserModel(**details.dict())
    db_user.password = Hash.hash_password(details.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user
