import base64
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from misc.func import find_item, gen_jid
from misc.miniapp import get_miniapp_code
from misc.model import model_map
from models import get_db
from models.jump import Jump

router = APIRouter()


class JumpGo(BaseModel):
    id: str
    idn: Literal["nid", "egid", "eid"]
    type: Literal["union", "examgroup", "exam"]


@router.get("/go")
def go_jump(id: str, db: Session = Depends(get_db)):
    jump = db.query(Jump).filter_by(jid=id).first()

    if not jump:
        raise HTTPException(status_code=404, detail="未找到资源。")

    mp = list(model_map.items())[jump.type]
    go = JumpGo(type=mp[0], idn=mp[1][1], id=jump.target)

    return go


class JumpGenerate(BaseModel):
    id: str
    type: Literal["union", "examgroup", "exam"]


class JumpFull(BaseModel):
    jid: str
    qrcode: str


@router.post("/generate")
def generate_jump(data: JumpGenerate, db: Session = Depends(get_db)):
    type = find_item(list(model_map.items()), lambda x: x[0], data.type)

    exists = db.query(Jump).filter_by(target=data.id).filter_by(type=type).first()
    if exists:
        code = base64.b64encode(exists.qrcode)
        return JumpFull(jid=exists.jid, qrcode=code)

    jid = gen_jid()
    while db.query(Jump).filter_by(jid=jid).count():
        jid = gen_jid()

    qrcode = get_miniapp_code(jid)
    code = base64.b64encode(qrcode)
    new_jump = Jump(jid=jid, target=data.id, type=type, qrcode=qrcode)
    db.add(new_jump)
    db.commit()

    return JumpFull(jid=jid, qrcode=code)
