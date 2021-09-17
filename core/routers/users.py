from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm.session import Session

from ..config.session import get_db
from ..dependencies.validations import validate_registration
from ..schemas.userSchema import User, UserCreate, UserLogin, UserProfile
from ..repository.userRepo import (
    InvalidPasswordError,
    UserAlreadyExistException,
    UserDoesNotExistException,
    create_user,
    login_user,
)

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.post("/register", response_model=UserProfile)
async def create_account(
    details: UserCreate = Depends(validate_registration), db: Session = Depends(get_db)
):
    try:
        user = await create_user(db, details)
        return user
    except UserAlreadyExistException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=e.args[0])


@router.post("/login", response_model=User)
async def login(details: UserLogin, db: Session = Depends(get_db)):
    try:
        user = await login_user(db, details)
        return user
    except UserDoesNotExistException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.args[0])
    except InvalidPasswordError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=e.args[0])
