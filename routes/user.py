from datetime import timedelta
from hashlib import sha256
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from auth import create_access_token, verify_passwd
from models import get_db
from models.user import User

router = APIRouter()


class UserLogin(BaseModel):
    email: str = Field(description="Email of the user.")
    password: str = Field(description="The password for the user.")
    expires: Optional[int] = Field(
        gt=0,
        le=2592000,
        description="Time to expire the token. Default to 3600 seconds.",
        default=3600,
    )


class UserToken(BaseModel):
    access_token: str = Field(
        description="JWT Token for authorization. Store it and bear it when requesting."
    )
    token_type: str = "bearer"
    admin: bool = Field(description="User's permission.")


@router.post("/login", response_model=UserToken, tags=["user"])
def login(data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(email=data.email).first()
    if not user:
        raise HTTPException(status_code=400, detail="User not found.")
    if not verify_passwd(data.password, user.passwd):
        raise HTTPException(status_code=400, detail="Password incorrect.")

    token = create_access_token(
        user.uid, timedelta(seconds=data.expires), admin=user.admin
    )

    return UserToken(access_token=token, admin=user.admin)


@router.post("/token", response_model=UserToken, tags=["user"])
def token(data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter_by(email=data.username).first()
    if not user:
        raise HTTPException(status_code=400, detail="User not found.")
    if not verify_passwd(sha256(data.password.encode()).hexdigest(), user.passwd):
        raise HTTPException(status_code=400, detail="Password incorrect.")

    token = create_access_token(user.uid, timedelta(seconds=3600), admin=user.admin)

    return UserToken(access_token=token, admin=user.admin)
