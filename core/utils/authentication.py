import bcrypt
import jwt

from ..config.settings import settings


class Hash:
    def hash_password(password: str) -> str:
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(str.encode(password), salt)
        return hashed_password.decode()

    def verify_password(plain_password: str, hashed_password: str):
        return bcrypt.checkpw(str.encode(plain_password), str.encode(hashed_password))


class JWT:
    secret: str = settings.jwt_secret
    algorithm: str = settings.jwt_secret

    def generate_token(self, user) -> str:
        return jwt.encode(user, self.secret, algorithm=self.algorithm)

    def decode_token(self, token):
        return jwt.decode(token, self.secret, algorithms=[self.algorithm])


jwt_auth = JWT()
