from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship

from misc.func import gen_id

from . import Base


class Union(Base):
    __tablename__ = "unions"

    nid = Column(String(36), primary_key=True, index=True, default=gen_id)
    name = Column(String(128), index=True)
    views = Column(Integer, default=0)
    member = Column(Text)

    examgroups = relationship("ExamGroup")
