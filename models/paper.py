from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from misc.func import gen_id

from . import Base


class Paper(Base):
    __tablename__ = "papers"

    pid = Column(String(36), primary_key=True, index=True, default=gen_id)
    eid = Column(String(36), ForeignKey("exams.eid"))
    comment = Column(String(128))
    created_at = Column(DateTime, default=func.now())
    uploader_ip = Column(String(128))
    user_token = Column(String(36))
    views = Column(Integer, default=0)
    receipt = Column(Boolean, default=False)

    files = relationship("File")
