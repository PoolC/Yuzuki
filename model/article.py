# -*- coding: utf-8 -*-
from datetime import datetime

from bleach import linkify
from sqlalchemy import Boolean, Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from helper.md_ext import markdown_convert
from model.base import Base


class Article(Base):
    __tablename__ = "article"
    uid = Column(Integer(), primary_key=True)
    board_id = Column(Integer(), ForeignKey("board.uid"), nullable=False)
    board = relationship("Board")
    user_id = Column(Integer(), ForeignKey("user.uid"), nullable=False)
    user = relationship("User", foreign_keys=user_id)
    subject = Column(String(255))
    content = Column(Text())
    compiled_content = Column(Text())
    enabled = Column(Boolean, default=True)
    is_modified = Column(Boolean, default=False, onupdate=True)
    last_modified = Column(DateTime, onupdate=datetime.now)
    created_at = Column(DateTime, default=datetime.now)
    deleted_at = Column(DateTime)
    deleted_user_id = Column(Integer(), ForeignKey("user.uid"))
    deleted_user = relationship("User", foreign_keys=deleted_user_id)
    reply_count = Column(Integer())
    replies = relationship("Reply")

    def __init__(self, board, user, subject, content):
        self.board = board
        self.user = user
        self.subject = subject
        self.change_content(content)
        self.reply_count = 0

    def __repr__(self):
        return "<Article uid=%s, subject=%s>" % (self.uid, self.subject)

    def change_content(self, content):
        self.content = content
        self.compiled_content = linkify(markdown_convert(content), parse_email=True)