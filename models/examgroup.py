from misc.func import gen_id

from sqlalchemy import Column, ForeignKey, String, Date, Integer
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from . import Base


class ExamGroup(Base):
    __tablename__ = "examgroups"

    egid = Column(String(64), primary_key=True, index=True, default=gen_id)
    date = Column(Date, default=func.now())
    name = Column(String(128), index=True)
    nid = Column(String(64), ForeignKey("unions.nid"))
    views = Column(Integer, default=0)

    exams = relationship("Exam")
