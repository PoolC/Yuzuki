# -*- coding: utf-8 -*-
from datetime import datetime

from bleach import linkify

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from model.base import Base


class Chat(Base):
    __tablename__ = "chat"
    uid = Column(Integer(), primary_key=True)
    content = Column(String(255))
    user_id = Column(Integer, ForeignKey("user.uid"))
    user = relationship("User")
    created_at = Column(DateTime, default=datetime.now)

    def __init__(self, user, content):
        self.user = user
        self.content = linkify(content, parse_email=True)

    def to_dict(self):
        return {
            "uid": self.uid,
            "user_id": self.user_id,
            "user_nickname": self.user.nickname,
            "content": self.content,
            "created_at": self.created_at.strftime("%y-%m-%d %H:%M:%S"),
        }
