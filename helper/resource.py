# -*- coding: utf-8 -*-
from datetime import datetime

from jinja2 import Environment, FileSystemLoader
from twisted.web.resource import Resource
from twisted.web.http import FORBIDDEN

from helper.md_ext import MarkdownExtension
from helper.database import DatabaseHelper
from model.board import Board
from config import SITE_NAME


class YuzukiResource(Resource):
    dbsession = DatabaseHelper.session()
    board_meta = dict()
    query = dbsession.query(Board).filter(Board.classification == "somoim").order_by(Board.order.asc())
    board_meta["somoim"] = [(board.name, board.repr) for board in query.all()]
    query = dbsession.query(Board).filter(Board.classification == "normal").order_by(Board.order.asc())
    board_meta["normal"] = [(board.name, board.repr) for board in query.all()]
    dbsession.close()

    jinja2_ext = [
        MarkdownExtension,
    ]
    jinja2_env = Environment(loader=FileSystemLoader("template",
                                                     encoding="utf-8"),
                             extensions=jinja2_ext)
    jinja2_env.globals = {
        "site_name": SITE_NAME,
        "datetime": datetime,
        "board_meta": board_meta,
    }

    def render(self, request):
        request.initialize(self)
        # TODO: auto login
        result = Resource.render(self, request)
        request.finalize()
        return result.encode("UTF-8")

    @staticmethod
    def get_template(name, parent=None, glob=None):
        return YuzukiResource.jinja2_env.get_template(name, parent, glob)

    @staticmethod
    def render_template(name, request, context=None):
        if context == None:
            context = dict()
        is_anybody = request.user and any([group.name == "anybody" for group in request.user.groups])
        context["request"] = request
        context["is_anybody"] = is_anybody
        return YuzukiResource.get_template(name).render(context)

    @staticmethod
    def render_template_from_text(text, context=None):
        if context == None:
            context = dict()
        template = YuzukiResource.jinja2_env.from_string(text)
        return template.render(context).encode("utf-8")

    @staticmethod
    def generate_error_message(request, code, brief, detail):
        context = {
            "brief": brief,
            "detail": detail,
            "title": str(code) + " " + str(brief),
        }
        return YuzukiResource.render_template("error.html", request, context)


def need_login(f):
    def _render_wrapper(resource, request):
        if request.user:
            return f(resource, request)
        else:
            request.setResponseCode(FORBIDDEN)
            return YuzukiResource.generate_error_message(request,
                                                         FORBIDDEN,
                                                         "Forbidden",
                                                         u"로그인 한 사용자만 볼 수 있는 페이지입니다")

    return _render_wrapper


def need_admin_permission(f):
    def _render_wrapper(resource, request):
        if request.user and request.user.is_admin:
            return f(resource, request)
        else:
            request.setResponseCode(FORBIDDEN)
            return YuzukiResource.generate_error_message(request,
                                                         FORBIDDEN,
                                                         "Forbidden",
                                                         u"관리자만 볼 수 있는 페이지입니다")

    return _render_wrapper