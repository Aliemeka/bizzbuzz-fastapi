from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm.session import Session

from ..config.session import get_db
from ..dependencies.validations import validate_registration
from ..schemas.userSchema import User, UserCreate, UserProfile
from ..repository.userRepo import (
    UserAlreadyExistException,
    create_user,
)

router = APIRouter(prefix="/accounts", tags=["users"])


@router.post("/register", response_model=UserProfile)
async def create_account(
    details: UserCreate = Depends(validate_registration), db: Session = Depends(get_db)
):
    try:
        user = await create_user(db, details)
        return user
    except UserAlreadyExistException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=e.args[0])
