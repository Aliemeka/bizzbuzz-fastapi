import bcrypt
import re
from sqlalchemy.orm import Session

from ..schemas.userSchema import UserCreate
from ..models.userModel import User as UserModel


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(str.encode(password), salt)
    return hashed_password.decode()


def validate_email(input_string: str) -> bool:
    regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    return re.fullmatch(regex, input_string) != None


class UserAlreadyExistException(Exception):
    pass


class EmailValidationError(Exception):
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
    if not validate_email(details.email):
        raise EmailValidationError({"message": f"Invalid email", "field": "email"})
    if await email_exist(db, details.email):
        raise UserAlreadyExistException(
            {"message": "Email already exist", "field": "email"}
        )
    if await username_exist(db, details.username):
        raise UserAlreadyExistException(
            {"message": "Username already exist", "field": "username"}
        )

    db_user = UserModel(**details.dict())
    print(vars(db_user))
    db_user.password = hash_password(details.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user
