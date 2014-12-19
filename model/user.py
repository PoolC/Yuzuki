from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text
from sqlalchemy.orm import relationship
from model.base import Base


class User(Base):
    __tablename__ = "user"
    uid = Column(Integer(), primary_key=True)
    username = Column(String(255), index=True, unique=True, nullable=False)
    nickname = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    groups = relationship("Group", secondary="assoc_user_group")
    pd_realname = Column(String(255), nullable=False)
    pd_email = Column(String(255))
    pd_address = Column(String(255))
    pd_phone = Column(String(255))
    pd_hakbeon = Column(Integer())
    pd_bio = Column(Text())
    created_at = Column(DateTime(), default=datetime.now)
    is_admin = Column(Boolean)

    def __init__(self, username, nickname, password, pd_realname, pd_email=None, pd_address=None, pd_phone=None,
                 pd_hakbeon=None, pd_bio=None):
        self.username = username
        self.nickname = nickname
        self.password = password
        self.pd_realname = pd_realname
        self.pd_email = pd_email
        self.pd_address = pd_address
        self.pd_phone = pd_phone
        self.pd_hakbeon = pd_hakbeon
        self.pd_bio = pd_bio
