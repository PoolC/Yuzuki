# -*- coding: utf-8 -*-
from MySQLdb import escape_string
from sphinxit.core.helpers import BaseSearchConfig
from sphinxit.core.processor import Search

from model.article import Article
from model.reply import Reply


class SphinxitConfig(BaseSearchConfig):
    WITH_STATUS = False
    WITH_META = False


def _search(indices, query, board):
    query = escape_string(query.encode("utf-8"))
    sphinx_query = Search(indexes=indices, config=SphinxitConfig)
    sphinx_query = sphinx_query.match(query).limit(0, 100)
    if board:
        sphinx_filter = dict()
        sphinx_filter[board + "__eq"] = board.uid
        sphinx_query.filter(sphinx_filter)
    result = sphinx_query.ask()
    items = result["result"]["items"]
    item_ids = [item["id"] for item in items]
    return item_ids


def search_article(dbsession, query, board=None):
    article_ids = _search(["article_main", "article_delta"], query, board)
    db_query = dbsession.query(Article).filter(Article.uid.in_(article_ids)).order_by(Article.uid.desc())
    return db_query


def search_reply(dbsession, query, board=None):
    reply_ids = _search(["reply_main", "reply_delta"], query, board)
    db_query = dbsession.query(Reply).filter(Reply.uid.in_(reply_ids)).order_by(Reply.uid.desc())
    return db_query