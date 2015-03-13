# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import DB_CONNECTION_STRING
from model.base import Base

# import all models you defined here
from model.association.user_group import UserGroupAssociation
from model.article import Article
from model.article_record import ArticleRecord
from model.board import Board
from model.chat import Chat
from model.chat_kv import ChatKV
from model.group import Group
from model.metadata import MetaData
from model.reply import Reply
from model.reply_record import ReplyRecord
from model.user import User

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
