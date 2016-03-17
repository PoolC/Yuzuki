from sqlalchemy import Table, Column, Integer, ForeignKey
from model.base import Base

subscription_table = Table(
    "subscription", Base.metadata,
    Column("user", Integer, ForeignKey("user.uid")),
    Column("article", Integer, ForeignKey("article.uid"))
)
