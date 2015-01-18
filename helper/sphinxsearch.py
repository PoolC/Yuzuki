# -*- coding: utf-8 -*-
from sphinxit.core.helpers import BaseSearchConfig
from sphinxit.core.processor import Search

from model.article import Article
from model.reply import Reply


class SphinxitConfig(BaseSearchConfig):
    WITH_STATUS = False
    WITH_META = False


def _search(indices, query, board):
    sphinx_query = Search(indexes=indices, config=SphinxitConfig)
    sphinx_query = sphinx_query.match(query)
    if board:
        sphinx_query.filter(board_id__eq=board.uid)
    result = sphinx_query.ask()
    items = sorted(result["result"]["items"], key=lambda x: x["weight"], reverse=True)
    item_ids = [item["id"] for item in items]
    return item_ids


def search_article(dbsession, query, board=None):
    article_ids = _search(["article_main", "article_delta"], query, board)
    db_query = dbsession.query(Article).filter(Article.uid.in_(article_ids))
    return db_query


def search_reply(dbsession, query, board=None):
    reply_ids = _search(["reply_main", "reply_delta"], query, board)
    db_query = dbsession.query(Reply).filter(Reply.uid.in_(reply_ids))
    return db_query
