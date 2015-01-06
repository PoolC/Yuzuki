# -*- coding: utf-8 -*-
from twisted.web.http import NOT_FOUND, UNAUTHORIZED
from sqlalchemy.orm import subqueryload

from helper.resource import YuzukiResource
from model.board import Board
from model.article import Article
from exception import BadArgument


class BoardView(YuzukiResource):
    ARTICLE_PER_PAGE = 15

    def render_GET(self, request):
        name = request.get_argument("name")
        # user must be in "anybody" group with exception for "notice" board
        if name != "notice" and (
                    not request.user or not any([group.name == "anybody" for group in request.user.groups])):
            return self.generate_error_message(request,
                                               UNAUTHORIZED,
                                               "Unauthorized",
                                               u"회원만 게시판을 열람할 수 있습니다.")
        try:
            page = int(request.get_argument("page", "1"))
        except ValueError:
            raise BadArgument("page", request.get_argument("page"))
        query = request.dbsession.query(Board).filter(Board.name == name)
        result = query.all()
        if not result:
            return self.generate_error_message(request,
                                               NOT_FOUND,
                                               "Not Found",
                                               u"게시판 이름이 잘못되었습니다.")
        board = result[0]
        query = request.dbsession.query(Article) \
            .filter(Article.enabled == True) \
            .filter(Article.board == board) \
            .order_by(Article.uid.desc()) \
            .options(subqueryload(Article.user))
        start_idx = self.ARTICLE_PER_PAGE * (page - 1)
        end_idx = start_idx + self.ARTICLE_PER_PAGE - 1
        articles = query[start_idx:end_idx]
        context = {
            "articles": articles,
            "board": board,
            "page": page,
        }
        return self.render_template("board.html", request, context)