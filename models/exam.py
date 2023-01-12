from misc.func import gen_id

from sqlalchemy import Column, Date, ForeignKey, Integer, String, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from . import Base


class Exam(Base):
    __tablename__ = "exams"

    eid = Column(String(64), primary_key=True, index=True, default=gen_id)
    date = Column(Date, default=func.now())
    course = Column(Integer, default=0, index=True)
    grade = Column(Integer, default=0, index=True)
    egid = Column(String(64), ForeignKey("examgroups.egid"))
    views = Column(Integer, default=0)

    papers = relationship("Paper")
