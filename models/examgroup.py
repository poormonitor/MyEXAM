from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from misc.func import gen_id

from . import Base


class ExamGroup(Base):
    __tablename__ = "examgroups"

    egid = Column(String(36), primary_key=True, index=True, default=gen_id)
    date = Column(Date, default=func.now())
    name = Column(String(128), index=True)
    nid = Column(String(36), ForeignKey("unions.nid"))
    views = Column(Integer, default=0)

    exams = relationship("Exam")
    assigns = relationship("Assign")
