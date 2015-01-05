import logging
from logging.config import fileConfig

DEBUG = True
SITE_NAME = "PoolC"
DB_CONNECTION_STRING = 'sqlite:///sqlite.db'
logger = logging.getLogger()
fileConfig("logger.cnf")