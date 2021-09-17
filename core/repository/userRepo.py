from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import user

from ..schemas.userSchema import UserCreate, UserLogin, User
from ..models.userModel import User as UserModel
from ..utils.authentication import Hash, jwt_auth
from ..utils.validations import Validate


class UserAlreadyExistException(Exception):
    pass


class UserDoesNotExistException(Exception):
    pass


class InvalidPasswordError(Exception):
    pass


async def get_user_by_email(db: Session, email: str):
    db_user = db.query(UserModel).filter(UserModel.email == email).one_or_none()
    if db_user == None:
        return False
    return db_user


async def get_user_by_username(db: Session, username: str):
    db_user = db.query(UserModel).filter(UserModel.username == username).one_or_none()
    if db_user == None:
        return False
    return db_user


async def create_user(db: Session, details: UserCreate):
    if await get_user_by_username(db, details.email):
        raise UserAlreadyExistException(
            {"error": "Email already exist", "field": "email"}
        )
    if await get_user_by_username(db, details.username):
        raise UserAlreadyExistException(
            {"error": "Username already exist", "field": "username"}
        )

    db_user = UserModel(**details.dict())
    db_user.password = Hash.hash_password(details.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


async def login_user(db: Session, details: UserLogin):
    db_user: UserModel
    login = details.login
    password = details.password

    is_email = Validate.email_valid(login)
    if is_email:
        db_user = await get_user_by_email(db, login)
    else:
        db_user = await get_user_by_username(db, login)

    if db_user:
        if not Hash.verify_password(password, db_user.password):
            raise InvalidPasswordError(
                {"error": f"Invalid password", "field": "password"}
            )
        user = User(**vars(db_user))
        token = jwt_auth.generate_token(user.dict())
        return {"token": token, "user": str(user.id), "is_active": db_user.is_active}

    field_type = "email" if is_email else "username"
    raise UserDoesNotExistException(
        {"error": f"Cannot find any account that matches your {field_type}: {login}"}
    )
