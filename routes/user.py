from datetime import datetime, timedelta
from hashlib import sha256
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from config import Settings, get_config
from misc.auth import create_access_token, get_current_user, hash_passwd, verify_passwd
from models import get_db
from models.user import User

router = APIRouter()


class UserLogin(BaseModel):
    email: str
    password: str


class UserToken(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserRegister(BaseModel):
    email: str
    nick: str
    password: str


class UserPasswd(BaseModel):
    old: str
    new: str


@router.post("/login", response_model=UserToken, tags=["user"])
def login(data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(email=data.email).first()

    if not user:
        raise HTTPException(status_code=400, detail="用户未找到。")

    if not verify_passwd(data.password, user.passwd):
        raise HTTPException(status_code=400, detail="密码错误。")

    token = create_access_token(
        user.uid, timedelta(hours=2), admin=user.admin, nick=user.nick
    )

    return UserToken(access_token=token)


@router.post("/token", response_model=UserToken, tags=["user"])
def token(data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter_by(email=data.username).first()

    if not user:
        raise HTTPException(status_code=400, detail="用户未找到。")

    if not verify_passwd(sha256(data.password.encode()).hexdigest(), user.passwd):
        raise HTTPException(status_code=400, detail="密码错误。")

    token = create_access_token(
        user.uid, timedelta(hours=2), admin=user.admin, nick=user.nick
    )

    return UserToken(access_token=token)


@router.post("/reg", tags=["user"])
def register(
    data: UserRegister,
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_config),
):
    if not settings.REGISTER:
        raise HTTPException(status_code=400, detail="当前不允许注册。")

    current = db.query(User).filter_by(email=data.email).count()
    if current > 0:
        raise HTTPException(status_code=400, detail="邮箱已经注册。")

    hashed = hash_passwd(data.password)
    new_user = User(email=data.email, passwd=hashed, nick=data.nick)

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
        raise HTTPException(status_code=400, detail="原密码错误。")

    user.passwd = hash_passwd(data.new)
    db.commit()

    return {"result": "success"}
