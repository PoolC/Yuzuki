import logging
from logging.config import fileConfig

REPLY_PER_PAGE = 15
DEBUG = True
SITE_NAME = "PoolC"
DB_CONNECTION_STRING = 'sqlite:///sqlite.db'
logger = logging.getLogger()
fileConfig("logger.cnf")