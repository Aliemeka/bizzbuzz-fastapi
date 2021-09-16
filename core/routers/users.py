from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm.session import Session

from ..config.session import get_db
from ..schemas.userSchema import User, UserCreate, UserProfile
from ..repository.userRepo import (
    EmailValidationError,
    UserAlreadyExistException,
    create_user,
    validate_email,
)

router = APIRouter(prefix="/accounts", tags=["users"])


@router.post("/register", response_model=UserProfile)
async def create_account(details: UserCreate, db: Session = Depends(get_db)):
    try:
        user = await create_user(db, details)
        return user
    except EmailValidationError as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=e.args[0])
    except UserAlreadyExistException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=e.args[0])
