from misc.func import gen_id

from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime
from sqlalchemy.sql import func

from . import Base


class File(Base):
    __tablename__ = "files"

    fid = Column(String(64), primary_key=True, index=True, default=gen_id)
    name = Column(Text, index=True)
    ext = Column(String(8))
    type = Column(Integer, default=0, index=True)
    pid = Column(String(64), ForeignKey("papers.pid"))
    upload_time = Column(DateTime, default=func.now())
    views = Column(Integer, default=0)
