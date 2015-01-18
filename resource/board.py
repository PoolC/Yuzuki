# -*- coding: utf-8 -*-
from config import ARTICLE_PER_PAGE
from exception import Unauthorized
from helper.model_control import get_board, get_article_page
from helper.permission import is_anybody, can_write
from helper.resource import YuzukiResource
from helper.template import render_template


class Board(YuzukiResource):
    def render_GET(self, request):
        name = request.get_argument("name")
        if not (name == "notice" or is_anybody(request)):
            raise Unauthorized()
        page = request.get_argument_int("page", 1)
        board = get_board(request, name)
        articles = get_article_page(request, board, page)
        total_article_count = board.article_count
        page_total = total_article_count / ARTICLE_PER_PAGE
        if total_article_count % ARTICLE_PER_PAGE != 0:
            page_total = total_article_count / ARTICLE_PER_PAGE + 1
        context = {
            "items": articles,
            "board": board,
            "page": page,
            "page_total": page_total,
            "can_write": can_write(request, board),
        }
        return render_template("board.html", request, context)
