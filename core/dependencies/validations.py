from fastapi import Header, HTTPException, Path

from ..utils.validations import Validate, ValidationError
from ..config.typing import validate_uuid
from ..schemas.userSchema import UserCreate


async def verify_token(x_token: str = Header(...)):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def verify_key(x_key: str = Header(...)):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    return x_key


async def validate_id(id: str):
    if not validate_uuid(id):
        raise HTTPException(status_code=400, detail=f"Invalid id: `{id}`")
    return id


async def validate_registration(userDetails: UserCreate) -> UserCreate:
    try:
        Validate.validate_email(userDetails.email)
        Validate.validate_password(userDetails.password)
        return userDetails
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=e.args[0])
