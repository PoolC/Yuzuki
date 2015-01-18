# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String

from model.base import Base


class MetaData(Base):
    __tablename__ = "metadata"
    name = Column(String(255), primary_key=True)
    value = Column(Integer())
