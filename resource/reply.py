# -*- coding: utf-8 -*-
from datetime import datetime
import json

from twisted.web.http import NOT_FOUND, UNAUTHORIZED
from sqlalchemy.orm import subqueryload

from exception import BadArgument
from helper.resource import YuzukiResource
from model.article import Article
from model.reply import Reply
from model.reply_record import ReplyRecord
from config import REPLY_PER_PAGE


class ReplyParent(YuzukiResource):
    isLeaf = False

    def __init__(self):
        YuzukiResource.__init__(self)
        self.putChild("view", ReplyView())
        self.putChild("write", ReplyWrite())
        self.putChild("delete", ReplyDelete())
        self.putChild("edit", ReplyEdit())


class ReplyView(YuzukiResource):
    _REPLY_PER_PAGE = REPLY_PER_PAGE

    def render_GET(self, request):
        article_id = request.get_argument("article_id")
        try:
            page = int(request.get_argument("page", "1"))
        except ValueError:
            raise BadArgument("page", request.get_argument("page"))
        query = request.dbsession.query(Article) \
            .filter(Article.uid == article_id) \
            .filter(Article.enabled == True) \
            .options(subqueryload(Article.board))
        result = query.all()
        if not result:
            request.setResponseCode(NOT_FOUND)
            return "article not found"
        article = result[0]
        if article.board.name == "notice" or (
                    request.user and any([group.name == "anybody" for group in request.user.groups])):
            query = request.dbsession.query(Reply) \
                .filter(Reply.article == article) \
                .filter(Reply.enabled == True) \
                .order_by(Reply.uid.desc()) \
                .options(subqueryload(Reply.user))
            start_idx = self._REPLY_PER_PAGE * (page - 1)
            end_idx = start_idx + self._REPLY_PER_PAGE
            result = query[start_idx:end_idx]
            return json.dumps([reply.to_dict() for reply in result])
        else:
            request.setResponseCode(UNAUTHORIZED)
            return "unauthorized"


class ReplyWrite(YuzukiResource):
    def render_POST(self, request):
        article_id = request.get_argument("article_id")
        query = request.dbsession.query(Article) \
            .filter(Article.uid == article_id) \
            .filter(Article.enabled == True) \
            .options(subqueryload(Article.board))
        result = query.all()
        if not result:
            request.setResponseCode(NOT_FOUND)
            return self.generate_error_message(request,
                                               NOT_FOUND,
                                               "Not Found",
                                               u"게시글이 존재하지 않습니다.")
        article = result[0]
        if request.user and request.user in article.board.comment_group.users:
            content = request.get_argument("content")
            # no empty reply
            if content.strip():
                reply = Reply(article, request.user, content)
                request.dbsession.add(reply)
                article.reply_count += 1
                request.dbsession.commit()
                page = request.get_argument("page", None)
                redirect = "/article/view?id=%s" % article.uid
                if page:
                    redirect += "&page=%s" % page
                request.redirect(redirect)
                return "success"
            else:
                raise BadArgument("content", "empty")
        else:
            request.setResponseCode(UNAUTHORIZED)
            return self.generate_error_message(request,
                                               UNAUTHORIZED,
                                               "Unauthorized",
                                               u"댓글을 쓸 권한이 없습니다.")


class ReplyDelete(YuzukiResource):
    def render_DELETE(self, request):
        reply_id = request.get_argument("id")
        query = request.dbsession.query(Reply) \
            .filter(Reply.uid == reply_id) \
            .filter(Reply.enabled == True) \
            .options(subqueryload(Reply.user))
        result = query.all()
        if not result:
            request.setResponseCode(NOT_FOUND)
            return "reply not found"
        reply = result[0]
        if request.user and (request.user == reply.user or request.user.is_admin):
            reply.enabled = False
            reply.deleted_at = datetime.now()
            reply.deleted_user = request.user
            reply.article.reply_count -= 1
            request.dbsession.commit()
            return "success"
        else:
            request.setResponseCode(UNAUTHORIZED)
            return "unauthorized"


class ReplyEdit(YuzukiResource):
    def render_POST(self, request):
        reply_id = request.get_argument("id")
        query = request.dbsession.query(Reply) \
            .filter(Reply.uid == reply_id) \
            .filter(Reply.enabled == True) \
            .options(subqueryload(Reply.user))
        result = query.all()
        if not result:
            request.setResponseCode(NOT_FOUND)
            return "reply not found"
        reply = result[0]
        if request.user and request.user == reply.user:
            content = request.get_argument("content")
            if content.strip():
                reply_record = ReplyRecord(reply)
                reply.content = content
                request.dbsession.add(reply_record)
                request.dbsession.commit()
                return "reply edit success"
            else:
                raise BadArgument("content", "empty")
        else:
            request.setResponseCode(UNAUTHORIZED)
            return "unauthorized"