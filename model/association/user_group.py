# -*- coding: utf-8 -*-
from sqlalchemy import Column, ForeignKey, Integer

from model.base import Base

class UserGroupAssociation(Base):
    __tablename__ = "assoc_user_group"
    user_id = Column(Integer(), ForeignKey("user.uid"), primary_key=True)
    group_id = Column(Integer(), ForeignKey("group.uid"), primary_key=True)