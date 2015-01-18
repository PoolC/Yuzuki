# -*- coding: utf-8 -*-
from jinja2 import escape
from sqlalchemy.orm import subqueryload

from helper.resource import YuzukiResource
from helper.template import render_template
from model.article import Article
from model.reply import Reply


class New(YuzukiResource):
    NEW_COUNT = 100

    def render_GET(self, request):
        articles = request.dbsession.query(Article).filter(Article.enabled).order_by(Article.uid.desc()).options(
            subqueryload(Article.user))[0:self.NEW_COUNT]
        replies = request.dbsession.query(Reply).filter(Reply.enabled).order_by(Reply.uid.desc()).options(
            subqueryload(Reply.user))[0:self.NEW_COUNT]
        articles_packed = [pack_article(article) for article in articles]
        replies_packed = [pack_reply(reply) for reply in replies]
        items = list()
        items.extend(articles_packed)
        items.extend(replies_packed)
        items = sorted(items, key=lambda i: i["created_at"], reverse=True)[0:self.NEW_COUNT]
        context = {"items": items}
        return render_template("new.html", request, context)


def pack_reply(reply):
    item = dict()
    item["article_id"] = reply.article_id
    item["type"] = u"댓"
    item["content"] = reply.content
    item["user"] = reply.user
    item["created_at"] = reply.created_at
    return item


def pack_article(article):
    item = dict()
    item["article_id"] = article.uid
    item["type"] = u"글"
    item["content"] = escape(article.subject)
    item["user"] = article.user
    item["created_at"] = article.created_at
    return item
