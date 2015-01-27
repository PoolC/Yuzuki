# -*- coding: utf-8 -*-
from datetime import datetime

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

    def to_dict(self):
        return {
            "uid": self.uid,
            "user_id": self.user_id,
            "user_nickname": self.user.nickname,
            "content": self.content,
            "created_at": self.created_at.strftime("%y-%m-%d %H:%M:%S"),
            "user_chat_color": self.user.chat_color,
        }
