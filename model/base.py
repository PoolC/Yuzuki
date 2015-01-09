# -*- coding: utf-8 -*-
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
Base.__table_args__ = {
    "mysql_charset": "utf8",
    "mysql_collate": "utf8_general_ci",
}