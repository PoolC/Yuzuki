# -*- coding: utf-8 -*-
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from model.base import Base


class ChatKV(Base):
    __tablename__ = "chat_kv"
    key = Column(String(255), primary_key=True)
    value = Column(Text())
    user_id = Column(Integer(), ForeignKey("user.uid"))
    user = relationship("User")
    created_at = Column(DateTime(), default=datetime.now)
