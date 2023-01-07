from misc.func import gen_id

from sqlalchemy import Boolean, Column, String

from . import Base


class User(Base):
    __tablename__ = "users"

    uid = Column(String(64), primary_key=True, index=True, default=gen_id)
    passwd = Column(String(64))
    email = Column(String(64))
    admin = Column(Boolean, default=False)
