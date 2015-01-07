# -*- coding: utf-8 -*-
from twisted.web.http import NOT_FOUND

from sqlalchemy.orm import subqueryload

from helper.resource import YuzukiResource
from model.article import Article


class ArticleParent(YuzukiResource):
    isLeaf = False

    def __init__(self):
        YuzukiResource.__init__(self)
        self.putChild("view", ArticleView())
        self.putChild("write", ArticleWrite())
        self.putChild("delete", ArticleDelete())


class ArticleView(YuzukiResource):
    def render_GET(self, request):
        article_id = request.get_argument("id")
        page = request.get_argument("page", None)
        query = request.dbsession.query(Article). \
            filter(Article.uid == article_id). \
            filter(Article.enabled == True). \
            options(subqueryload(Article.board))
        result = query.all()
        if not result:
            request.setResponseCode(NOT_FOUND)
            return self.generate_error_message(request,
                                               NOT_FOUND,
                                               "Not Found",
                                               u"게시글이 존재하지 않습니다.")
        article = result[0]
        context = {
            "article": article,
            "page": page,
        }
        return self.render_template("article_view.html", request, context)


class ArticleWrite(YuzukiResource):
    pass


class ArticleDelete(YuzukiResource):
    pass