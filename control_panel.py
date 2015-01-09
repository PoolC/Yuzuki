# -*- coding: utf-8 -*-
from helper.database import DatabaseHelper

dbsession = DatabaseHelper.session()

from model.article import Article
from model.article_record import ArticleRecord
from model.association.user_group import UserGroupAssociation
from model.board import Board
from model.group import Group
from model.reply import Reply
from model.reply_record import ReplyRecord
from model.user import User

anybody = dbsession.query(Group).filter(Group.name == "anybody")[0]

import code
code.interact(local=locals())