from sqlalchemy import Boolean, Column, String, Text

from misc.func import gen_id

from . import Base


class User(Base):
    __tablename__ = "users"

    uid = Column(String(36), primary_key=True, index=True, default=gen_id)
    nick = Column(String(32))
    passwd = Column(String(64))
    email = Column(String(64))
    admin = Column(Boolean, default=False)
    cart = Column(Text)
