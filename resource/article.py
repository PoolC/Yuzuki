# -*- coding: utf-8 -*-
from datetime import datetime

from twisted.web.http import NOT_FOUND, UNAUTHORIZED
from sqlalchemy.orm import subqueryload

from helper.resource import YuzukiResource
from model.article import Article
from model.article_record import ArticleRecord
from model.board import Board
from model.reply import Reply
from exception import BadArgument
from config import REPLY_PER_PAGE

class ArticleParent(YuzukiResource):
    isLeaf = False

    def __init__(self):
        YuzukiResource.__init__(self)
        self.putChild("view", ArticleView())
        self.putChild("write", ArticleWrite())
        self.putChild("delete", ArticleDelete())
        self.putChild("edit", ArticleEdit())


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
        if article.board.name == "notice" or (
                    request.user and any([group.name == "anybody" for group in request.user.groups])):
            reply_count = self.dbsession.query(Reply).filter(Reply.enabled == True).filter(
                Reply.article == article).count()
            reply_page_total = reply_count / REPLY_PER_PAGE
            if reply_count % REPLY_PER_PAGE != 0:
                reply_page_total += 1
            context = {
                "article": article,
                "page": page,
                "reply_page_total": reply_page_total,
            }
            return self.render_template("article_view.html", request, context)
        else:
            request.setResponseCode(UNAUTHORIZED)
            return self.generate_error_message(request,
                                               UNAUTHORIZED,
                                               "Unauthorized",
                                               u"게시글을 볼 권한이 없습니다.")


class ArticleWrite(YuzukiResource):
    def render_GET(self, request):
        if request.user and any([group.name == "anybody" for group in request.user.groups]):
            board_name = request.get_argument("name")
            query = request.dbsession.query(Board).filter(Board.name == board_name)
            result = query.all()
            if not result:
                request.setResponseCode(NOT_FOUND)
                return self.generate_error_message(request,
                                                   UNAUTHORIZED,
                                                   "Unauthorized",
                                                   u"게시판이 존재하지 않습니다.")
            board = result[0]
            context = {"board": board}
            return self.render_template("article_write.html", request, context)
        else:
            request.setResponseCode(UNAUTHORIZED)
            return self.generate_error_message(request,
                                               UNAUTHORIZED,
                                               "Unauthorized",
                                               u"회원만 게시글을 쓸 수 있습니다.")

    def render_POST(self, request):
        if request.user:
            board_name = request.get_argument("name")
            query = request.dbsession.query(Board).filter(Board.name == board_name)
            result = query.all()
            if not result:
                request.setResponseCode(NOT_FOUND)
                return self.generate_error_message(request,
                                                   NOT_FOUND,
                                                   "Not Found",
                                                   u"게시판이 존재하지 않습니다.")
            board = result[0]
            if request.user in board.write_group.users:
                subject = request.get_argument("subject")
                content = request.get_argument("content")
                # no empty subject
                if subject.strip():
                    article = Article(board, request.user, subject, content)
                    request.dbsession.add(article)
                    request.dbsession.commit()
                    request.redirect("/article/view?id=%s" % article.uid)
                    return "article posted"
                else:
                    raise BadArgument("subject", "empty")
            else:
                request.setResponseCode(UNAUTHORIZED)
                return self.generate_error_message(request,
                                                   UNAUTHORIZED,
                                                   "Unauthorized",
                                                   u"글쓰기 권한이 없습니다.")
        else:
            request.setResponseCode(UNAUTHORIZED)
            return self.generate_error_message(request,
                                               UNAUTHORIZED,
                                               "Unauthorized",
                                               u"회원만 게시글을 쓸 수 있습니다.")


class ArticleDelete(YuzukiResource):
    def render_DELETE(self, request):
        article_id = request.get_argument("id")
        query = request.dbsession.query(Article). \
            filter(Article.uid == article_id). \
            filter(Article.enabled == True). \
            options(subqueryload(Article.board))
        result = query.all()
        if not result:
            request.setResponseCode(NOT_FOUND)
            return "article not found"
        article = result[0]
        if request.user and (request.user == article.user or request.user.is_admin):
            article.enabled = False
            article.deleted_at = datetime.now()
            article.deleted_user = request.user
            request.dbsession.commit()
            return "delete success"
        else:
            request.setResponseCode(UNAUTHORIZED)
            return "unauthorized user"


class ArticleEdit(YuzukiResource):
    def render_GET(self, request):
        article_id = request.get_argument("id")
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
        if request.user and request.user == article.user:
            context = {"article": article}
            return self.render_template("article_edit.html", request, context)
        else:
            request.setResponseCode(UNAUTHORIZED)
            return self.generate_error_message(request,
                                               UNAUTHORIZED,
                                               "Unauthorized",
                                               u"게시글을 수정할 권한이 없습니다.")

    def render_POST(self, request):
        article_id = request.get_argument("id")
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
        if request.user and request.user == article.user:
            subject = request.get_argument("subject")
            content = request.get_argument("content")
            # no empty subject
            if subject.strip():
                article_record = ArticleRecord(article)
                article.subject = subject
                article.change_content(content)
                request.dbsession.add(article_record)
                request.dbsession.commit()
                request.redirect("/article/view?id=%s" % article.uid)
                return "article edit success"
            else:
                raise BadArgument("subject", "empty")
        else:
            request.setResponseCode(UNAUTHORIZED)
            return self.generate_error_message(request,
                                               UNAUTHORIZED,
                                               "Unauthorized",
                                               u"게시글을 수정할 권한이 없습니다.")