from sqlalchemy import Column, DateTime, String, Text, Float
from sqlalchemy.sql import func

from misc.func import gen_id

from . import Base


class Task(Base):
    __tablename__ = "tasks"

    tid = Column(String(36), primary_key=True, index=True, default=gen_id)
    type = Column(String(8), index=True)
    data = Column(Text)
    status = Column(Float, default=0)
    created = Column(DateTime, default=func.now(), index=True)
