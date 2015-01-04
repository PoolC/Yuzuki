# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from model.base import Base


class Group(Base):
    __tablename__ = "group"
    uid = Column(Integer(), primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(String(255))
    users = relationship("User", secondary="assoc_user_group")

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Group name=%s>" % self.name