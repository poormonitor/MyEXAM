from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.sql import func

from misc.func import gen_id

from . import Base


class Assign(Base):
    __tablename__ = "assigns"

    aid = Column(String(36), primary_key=True, index=True, default=gen_id)
    egid = Column(String(36), ForeignKey("examgroups.egid"))
    comment = Column(String(128))
    views = Column(Integer, default=0)
    md5 = Column(String(32), index=True)
    upload_time = Column(DateTime, default=func.now())
    ext = Column(String(8))
