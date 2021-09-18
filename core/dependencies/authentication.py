from core.models.userModel import User
from fastapi import Request, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from ..utils.authentication import InvalidTokenException, TokenExpired, jwt_auth


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(
            JWTBearer, self
        ).__call__(request)

        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403, detail="Invalid authentication scheme"
                )
            user = self.verify_token(credentials.credentials)
            return user
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_token(self, token: str) -> User:
        try:
            user = jwt_auth.decode_token(token)
            return user
        except InvalidTokenException as e:
            raise HTTPException(status_code=401, detail=e.args[0]["error"])
        except TokenExpired as e:
            raise HTTPException(status_code=401, detail=e.args[0]["error"])
