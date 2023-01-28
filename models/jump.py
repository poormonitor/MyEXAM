from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.sql import func

from misc.func import gen_jid

from . import Base


class Jump(Base):
    __tablename__ = "jumps"

    jid = Column(String(6), primary_key=True, index=True, default=gen_jid)
    target = Column(String(32), index=True)
    type = Column(Integer, index=True)
    created = Column(DateTime, default=func.now())
    qrcode = Column(Text)
