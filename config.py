import logging
from logging.config import fileConfig

DEBUG = False
DB_CONNECTION_STRING = 'sqlite:///:memory:'
logger = logging.getLogger()
fileConfig("logger.cnf")