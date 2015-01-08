from helper.database import DatabaseHelper

dbsession = DatabaseHelper.session()

from model.user import User
from model.group import Group
from model.association.user_group import UserGroupAssociation
from model.board import Board
from model.article import Article
from model.reply import Reply
from model.article_record import ArticleRecord
from model.reply_record import ReplyRecord

anybody = dbsession.query(Group).filter(Group.name == "anybody")[0]

import code
code.interact(local=locals())