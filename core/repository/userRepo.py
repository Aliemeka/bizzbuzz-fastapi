from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import user

from ..schemas.userSchema import UserCreate, UserLogin, User
from ..schemas.tokenSchema import Token
from ..models.userModel import User as UserModel
from ..utils.authentication import Hash, jwt_auth
from ..utils.validations import Validate
from ..utils.mailservice import send_email


class UserAlreadyExistException(Exception):
    pass


class UserDoesNotExistException(Exception):
    pass


class InvalidPasswordError(Exception):
    pass


async def get_user_by_id(db: Session, id: str):
    return db.query(UserModel).filter(UserModel.id == id).one_or_none()


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
    if await get_user_by_username(db, details.email) or await get_user_by_username(
        db, details.username
    ):
        raise UserAlreadyExistException(
            {"error": "Email already exist", "field": "email"}
        )

    db_user = UserModel(**details.dict())
    db_user.password = Hash.hash_password(details.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    await send_email(
        db_user,
        f"Welcome to Bizzbuzz {db_user.first_name + ' ' + db_user.last_name}",
        "Welcome to BizzBuzz",
    )
    return db_user


async def login_user(db: Session, details: UserLogin) -> Token:
    db_user: UserModel
    login = details.login
    password = details.password

    is_email = Validate.email_valid(login)
    db_user = (
        await get_user_by_email(db, login)
        if is_email
        else await get_user_by_username(db, login)
    )

    if db_user:
        if not Hash.verify_password(password, db_user.password):
            raise InvalidPasswordError(
                {"error": f"Invalid password", "field": "password"}
            )
        user = User(**vars(db_user))
        token = jwt_auth.generate_token(user.dict())
        return Token(
            **{
                "token": token,
                "user": str(user.id),
                "expires": jwt_auth.get_expiry_time(),
                "is_active": db_user.is_active,
            }
        )

    field_type = "email" if is_email else "username"
    raise UserDoesNotExistException(
        {"error": f"Cannot find any account that matches your {field_type}: {login}"}
    )
