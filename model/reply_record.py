from datetime import datetime

from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from model.base import Base


class ReplyRecord(Base):
    __tablename__ = "reply_record"
    uid = Column(Integer(), primary_key=True)
    reply_id = Column(Integer(), ForeignKey("reply.uid"))
    reply = relationship("Reply")
    content = Column(Text())
    created_at = Column(DateTime, default=datetime.now)

    def __init__(self, reply):
        self.reply = reply
        self.content = reply.content

    def __repr__(self):
        return "<ReplyRecord uid=%s, content=%s>" % (self.uid, self.content)