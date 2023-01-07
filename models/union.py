from misc.func import gen_id

from sqlalchemy import Column, String, Text, Integer
from sqlalchemy.orm import relationship

from . import Base


class Union(Base):
    __tablename__ = "unions"

    nid = Column(String(64), primary_key=True, index=True, default=gen_id)
    name = Column(String(128), index=True)
    views = Column(Integer, default=0)
    member = Column(Text)

    examgroups = relationship("ExamGroup")
