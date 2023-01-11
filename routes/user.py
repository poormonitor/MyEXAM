from datetime import timedelta
from hashlib import sha256
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from auth import create_access_token, get_current_user, hash_passwd, verify_passwd
from config import Settings, get_config
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


class UserLoginResult(BaseModel):
    access_token: str = Field(
        description="JWT Token for authorization. Store it and bear it when requesting."
    )
    nick: str = Field(description="User's nickname.")
    admin: bool = Field(description="User's permission.")
    uid: str = Field(description="User's uid.")


class UserRegister(BaseModel):
    email: str
    password: str


class UserPasswd(BaseModel):
    old: str
    new: str


@router.post("/login", response_model=UserLoginResult, tags=["user"])
def login(data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(email=data.email).first()
    if not user:
        raise HTTPException(status_code=400, detail="User not found.")
    if not verify_passwd(data.password, user.passwd):
        raise HTTPException(status_code=400, detail="Password incorrect.")

    token = create_access_token(
        user.uid, timedelta(seconds=data.expires), admin=user.admin, nick=user.nick
    )
    
    return UserLoginResult(
        access_token=token, admin=user.admin, uid=user.uid, nick=user.nick
    )


@router.post("/token", response_model=UserToken, tags=["user"])
def token(data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter_by(email=data.username).first()
    if not user:
        raise HTTPException(status_code=400, detail="User not found.")
    if not verify_passwd(sha256(data.password.encode()).hexdigest(), user.passwd):
        raise HTTPException(status_code=400, detail="Password incorrect.")

    token = create_access_token(
        user.uid, timedelta(seconds=3600), admin=user.admin, nick=user.nick
    )

    return UserToken(access_token=token)


@router.post("/reg", tags=["user"])
def register(
    data: UserRegister,
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_config),
):
    if not settings.REGISTER:
        raise HTTPException(status_code=400, detail="Registering is not allowed now.")

    current = db.query(User).filter_by(email=data.email).count()
    if current > 0:
        raise HTTPException(status_code=400, detail="The email exists.")

    hashed = hash_passwd(data.password)
    new_user = User(email=data.email, passwd=hashed)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"result": "success"}


@router.post("/passwd", tags=["user"])
def passwd(
    data: UserPasswd,
    db: Session = Depends(get_db),
    uid: str = Depends(get_current_user),
):
    user = db.query(User).filter_by(uid=uid).first()

    if not verify_passwd(data.old, user.passwd):
        raise HTTPException(status_code=400, detail="The origin password is incorrect.")

    user.passwd = hash_passwd(data.new)
    db.commit()

    return {"result": "success"}
