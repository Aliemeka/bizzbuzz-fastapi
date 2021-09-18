import bcrypt
import jwt
from datetime import datetime, timedelta
from typing import TypedDict

from sqlalchemy.sql.functions import user

from ..config.settings import settings
from ..schemas.userSchema import User


class UserDict(TypedDict):
    id: str
    first_name: str
    last_name: str
    username: str
    email: str
    exp: datetime


class TokenExpired(Exception):
    pass


class InvalidTokenException(Exception):
    pass


class Hash:
    def hash_password(password: str) -> str:
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(str.encode(password), salt)
        return hashed_password.decode()

    def verify_password(plain_password: str, hashed_password: str):
        return bcrypt.checkpw(str.encode(plain_password), str.encode(hashed_password))


class JWT:
    secret: str = settings.jwt_secret
    algorithm: str = settings.algorithm
    expiry_time: datetime

    def generate_token(self, user: dict) -> str:
        self.expiry_time = datetime.utcnow() + timedelta(minutes=120)
        user["id"] = str(user["id"])
        user["exp"] = self.expiry_time
        user_dict: UserDict = user.copy()
        return jwt.encode(user_dict, self.secret, algorithm=self.algorithm)

    def decode_token(self, token: str):
        try:
            user_dict: UserDict = jwt.decode(
                token, self.secret, algorithms=[self.algorithm]
            )
            user_dict["exp"] = datetime.fromtimestamp(user_dict["exp"])
            if user_dict["exp"] >= datetime.utcnow():
                return User(**user_dict)
            else:
                raise TokenExpired({"error": "Access token has expired"})
        except:
            raise InvalidTokenException({"error": "Invalid token"})

    def get_expiry_time(self):
        return self.expiry_time


jwt_auth = JWT()
