from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.sql import or_

from misc.auth import hash_passwd
from models import get_db
from models.user import User

router = APIRouter()


class Users(BaseModel):
    uid: str
    nick: str
    email: str
    admin: bool


class DelUser(BaseModel):
    uid: str


class PasswdModify(BaseModel):
    uid: str
    passwd: str


class SwitchAdmin(BaseModel):
    uid: str
    admin: bool


@router.get("/list")
def list_users(s: str = "", page: int = 0, db: Session = Depends(get_db)):
    query = db.query(User).filter(or_(User.nick.contains(s), User.email.contains(s)))

    cnt = query.count()
    users = query.offset(page * 10).limit(10).all()

    return {"cnt": cnt, "users": [Users(**vars(i)) for i in users]}


@router.post("/delete")
def delete_user(data: DelUser, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(uid=data.uid).first()

    if not user:
        raise HTTPException(status_code=404, detail="用户未找到。")

    db.delete(user)
    db.commit()
    return {"result": "success"} 


@router.post("/passwd")
def modify_password(data: PasswdModify, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(uid=data.uid).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户未找到。")

    user.passwd = hash_passwd(data.passwd)
    db.commit()
    return {"result": "success"}


@router.post("/admin")
def switch_admin(data: SwitchAdmin, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(uid=data.uid).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户未找到。")

    user.admin = data.admin
    db.commit()
    return {"result": "success"}
