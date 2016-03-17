# -*- coding: utf-8 -*-
import json

from exception import BadRequest, Unauthorized
from helper.model_control import get_article, get_reply_page, get_reply,\
    delete_reply, edit_reply, create_reply
from helper.permission import is_anybody, can_comment, is_author_or_admin,\
    is_author
from helper.resource import YuzukiResource, need_anybody_permission
from helper.slack import post_messages_to_subscribers


class ReplyParent(YuzukiResource):
    isLeaf = False

    def __init__(self):
        YuzukiResource.__init__(self)
        self.putChild("view", ReplyView())
        self.putChild("write", ReplyWrite())
        self.putChild("delete", ReplyDelete())
        self.putChild("edit", ReplyEdit())


class ReplyView(YuzukiResource):
    def render_GET(self, request):
        article_id = request.get_argument("article_id")
        page = request.get_argument_int("page", 1)
        article = get_article(request, article_id)
        if article.board.name == "notice" or (is_anybody(request)):
            replies = get_reply_page(request, article, page)
            return json.dumps([reply.to_dict() for reply in replies])
        else:
            raise Unauthorized()


class ReplyWrite(YuzukiResource):
    @need_anybody_permission
    def render_POST(self, request):
        article_id = request.get_argument("article_id")
        article = get_article(request, article_id)
        if not can_comment(request, article.board):
            raise Unauthorized()
        content = request.get_argument("content")
        # no empty reply
        if content.strip():
            reply = create_reply(request, article, content)
            request.dbsession.add(reply)
            request.dbsession.commit()
            page = request.get_argument("page", None)
            redirect = "/article/view?id=%s" % article.uid
            if page:
                redirect += "&page=%s" % page
            post_messages_to_subscribers(request, article.subscribing_users,
                                         u"구독하고 있는 글에 새 댓글이 등록되었습니다.",
                                         reply.user, article.subject,
                                         content, redirect)
            request.redirect(redirect)
            return "success"
        else:
            raise BadRequest()


class ReplyDelete(YuzukiResource):
    @need_anybody_permission
    def render_DELETE(self, request):
        reply_id = request.get_argument("id")
        reply = get_reply(request, reply_id)
        if is_author_or_admin(request, reply):
            delete_reply(request, reply)
            request.dbsession.commit()
            return "success"
        else:
            raise Unauthorized()


class ReplyEdit(YuzukiResource):
    @need_anybody_permission
    def render_POST(self, request):
        reply_id = request.get_argument("id")
        reply = get_reply(request, reply_id)
        if is_author(request, reply):
            content = request.get_argument("content")
            if content.strip():
                edit_reply(request, reply, content)
                request.dbsession.commit()
                return "reply edit success"
            else:
                raise BadRequest()
        else:
            raise Unauthorized()
