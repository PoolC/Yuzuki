# -*- coding: utf-8 -*-
import logging
import os
from logging.config import fileConfig

ARTICLE_PER_PAGE = 15
REPLY_PER_PAGE = 15
CHAT_PER_PAGE = 20
CHAT_CONNECTION_INTERVAL = 30
DEBUG = False
DB_CONNECTION_STRING = "sqlite:///sqlite.db"
USE_REDIS = False
REDIS_CONNECT_ARGS = {
    "host": "localhost",
    "port": 6379,
    "db": 0,
}
SLACK_POST_INFO = {
    "username": "bot",
    "token": "",
    "as_user": False
}
SLACK_NOTI_CHANNEL = '#general'
SLACK_NOTI_TARGET_BOARDS = ()
logger = logging.getLogger()
if not os.path.exists("log"):
    os.mkdir("log")
fileConfig("logger.cnf")
