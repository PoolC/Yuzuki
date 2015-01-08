import cgi
from datetime import datetime

from sqlalchemy import Boolean, Column, Integer, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from model.base import Base


class Reply(Base):
    __tablename__ = "reply"
    uid = Column(Integer(), primary_key=True)
    article_id = Column(Integer(), ForeignKey("article.uid"))
    article = relationship("Article")
    user_id = Column(Integer(), ForeignKey("user.uid"))
    user = relationship("User")
    content = Column(Text())
    enabled = Column(Boolean, default=True)
    is_modified = Column(Boolean, default=False, onupdate=True)
    last_modified = Column(DateTime, onupdate=datetime.now)
    created_at = Column(DateTime, default=datetime.now)

    def __init__(self, article, user, content):
        self.article = article
        self.user = user
        self.content = cgi.escape(content)

    def __repr__(self):
        return "<Reply uid=%s, content=%s>" % (self.uid, self.content)

    def to_dict(self):
        data = {
            "uid": self.uid,
            "article_id": self.article_id,
            "user_id": self.user_id,
            "user_nickname": self.user.nickname,
            "content": self.content,
            "is_modified": self.is_modified,
            "created_at": self.created_at.strftime("%y-%m-%d %H:%M:%S"),
        }
        if self.is_modified:
            data["last_modified"] = self.last_modified.strftime("%y-%m-%d %H:%M:%S")
        return data