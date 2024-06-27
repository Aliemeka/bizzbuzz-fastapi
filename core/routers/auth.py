from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm.session import Session
from typing_extensions import TypedDict

from ..config.session import get_db
from ..dependencies.validations import validate_registration
from ..dependencies.authentication import JWTBearer
from ..schemas.userSchema import User, UserCreate, UserLogin, UserProfile
from ..schemas.tokenSchema import Token
from ..repository.userRepo import (
    InvalidPasswordError,
    UserAlreadyExistException,
    UserDoesNotExistException,
    change_password,
    create_user,
    login_user,
)

router = APIRouter(prefix="/auth", tags=["authentication"])
UpdatePasswordPayload = TypedDict(
    "UpdatePasswordPayload", current_password=str, new_password=str
)
Message = TypedDict("Success", message=str)


@router.post("/register", response_model=UserProfile)
async def create_account(
    details: UserCreate = Depends(validate_registration), db: Session = Depends(get_db)
):
    try:
        user = await create_user(db, details)
        return user
    except UserAlreadyExistException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=e.args[0])


@router.post("/login", response_model=Token)
async def login(details: UserLogin, db: Session = Depends(get_db)):
    try:
        response = await login_user(db, details)
        return response
    except UserDoesNotExistException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.args[0])
    except InvalidPasswordError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=e.args[0])


@router.post("/change-password", response_model=TypedDict("Success", message=str))
async def update_password(
    details: UpdatePasswordPayload,
    db: Session = Depends(get_db),
    user: User = Depends(JWTBearer()),
):
    try:
        await change_password(
            db, details["current_password"], details["new_password"], str(user.id)
        )
        return {"message": "Password updated successfully"}
    except UserDoesNotExistException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.args[0])
    except InvalidPasswordError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=e.args[0])
