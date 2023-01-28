from sqlalchemy import BLOB, Column, DateTime, Integer, String
from sqlalchemy.sql import func

from misc.func import gen_jid

from . import Base


class Jump(Base):
    __tablename__ = "jumps"

    jid = Column(String(6), primary_key=True, index=True, default=gen_jid)
    target = Column(String(36), index=True)
    type = Column(Integer, index=True)
    created = Column(DateTime, default=func.now())
    qrcode = Column(BLOB)
