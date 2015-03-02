# -*- coding: utf-8 -*-
from helper.database import DatabaseHelper

dbsession = DatabaseHelper.session()

from model.group import Group
from model.user import User

anybody = dbsession.query(Group).filter(Group.name == "anybody")[0]


def get_user_by_username(username):
    query = dbsession.query(User).filter(User.username == username)
    result = query.all()
    return result[0] if result else None


def get_user_by_uid(uid):
    query = dbsession.query(User).filter(User.uid == uid)
    result = query.all()
    return result[0] if result else None


def get_users_not_anybody():
    anybody_user_ids = [user.uid for user in anybody.users]
    query = dbsession.query(User).filter(User.uid.notin_(anybody_user_ids))
    return query.all()


import code

code.interact(local=locals())
