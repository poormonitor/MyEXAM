from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.sql import func

from misc.func import gen_id

from . import Base


class File(Base):
    __tablename__ = "files"

    fid = Column(String(36), primary_key=True, index=True, default=gen_id)
    name = Column(Text, index=True)
    md5 = Column(String(32), index=True)
    ext = Column(String(8))
    type = Column(Integer, default=0, index=True)
    pid = Column(String(36), ForeignKey("papers.pid"))
    upload_time = Column(DateTime, default=func.now())
    views = Column(Integer, default=0)
    ocr = Column(Text)
