from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from model.base import Base


class ArticleRecord(Base):
    __tablename__ = "article_record"
    uid = Column(Integer(), primary_key=True)
    article_id = Column(Integer(), ForeignKey("article.uid"))
    article = relationship("Article")
    subject = Column(String(255))
    content = Column(Text())
    created_at = Column(DateTime, default=datetime.now)

    def __init__(self, article):
        self.article = article
        self.subject = article.subject
        self.content = article.content

    def __repr__(self):
        return "<ArticleRecord uid=%s, subject=%s>" % (self.uid, self.subject)