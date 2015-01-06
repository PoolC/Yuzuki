# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import DB_CONNECTION_STRING
from model.base import Base

# import all models you defined here
from model.user import User
from model.group import Group
from model.association.user_group import UserGroupAssociation
from model.board import Board
from model.article import Article

class DatabaseHelper(object):
    _engine = create_engine(DB_CONNECTION_STRING)
    _Session = sessionmaker(bind=_engine)
    
    @classmethod
    def engine(cls):
        return cls._engine
    
    @classmethod
    def session(cls):
        return cls._Session()
    
    @classmethod
    def create_all(cls):
        Base.metadata.create_all(cls._engine)
    
    @classmethod
    def drop_all(cls):
        Base.metadata.drop_all(cls._engine)