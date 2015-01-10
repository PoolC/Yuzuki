# -*- coding: utf-8 -*-
from twisted.web.http import NOT_FOUND, UNAUTHORIZED
from sqlalchemy.orm import subqueryload

from config import ARTICLE_PER_PAGE
from exception import BadArgument
from helper.template import render_template, generate_error_message
from helper.resource import YuzukiResource
from model.board import Board
from model.article import Article


class BoardView(YuzukiResource):
    _ARTICLE_PER_PAGE = ARTICLE_PER_PAGE

    def render_GET(self, request):
        name = request.get_argument("name")
        # user must be in "anybody" group with exception for "notice" board
        if name != "notice" and (
                    not request.user or not any([group.name == "anybody" for group in request.user.groups])):
            request.setResponseCode(UNAUTHORIZED)
            return generate_error_message(request, UNAUTHORIZED, u"회원만 게시판을 열람할 수 있습니다.")
        try:
            page = int(request.get_argument("page", "1"))
        except ValueError:
            raise BadArgument()
        query = request.dbsession.query(Board).filter(Board.name == name)
        result = query.all()
        if not result:
            request.setResponseCode(NOT_FOUND)
            return generate_error_message(request, NOT_FOUND, u"게시판 이름이 잘못되었습니다.")
        board = result[0]
        query = request.dbsession.query(Article) \
            .filter(Article.enabled == True) \
            .filter(Article.board == board) \
            .order_by(Article.uid.desc()) \
            .options(subqueryload(Article.user))
        start_idx = self._ARTICLE_PER_PAGE * (page - 1)
        end_idx = start_idx + self._ARTICLE_PER_PAGE
        articles = query[start_idx:end_idx]
        total_article_count = query.count()
        if total_article_count % self._ARTICLE_PER_PAGE == 0:
            page_total = total_article_count / self._ARTICLE_PER_PAGE
        else:
            page_total = total_article_count / self._ARTICLE_PER_PAGE + 1
        can_write = request.user and board.write_group in request.user.groups
        context = {
            "articles": articles,
            "board": board,
            "page": page,
            "page_total": page_total,
            "can_write": can_write,
        }
        return render_template("board.html", request, context)