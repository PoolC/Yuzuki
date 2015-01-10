# -*- coding: utf-8 -*-
from datetime import datetime

from bleach import linkify

from sqlalchemy.orm import subqueryload

from config import ARTICLE_PER_PAGE, REPLY_PER_PAGE

from exception import PageNotFound
from model.article import Article
from model.article_record import ArticleRecord
from model.board import Board
from model.reply import Reply
from model.reply_record import ReplyRecord


def get_board(request, board_name):
    query = request.dbsession.query(Board).filter(Board.name == board_name)
    result = query.all()
    if not result:
        raise PageNotFound()
    return result[0]


def get_article(request, article_id):
    query = request.dbsession.query(Article).filter(Article.uid == article_id).filter(Article.enabled == True).options(
        subqueryload(Article.board)).options(subqueryload(Article.user))
    result = query.all()
    if not result:
        raise PageNotFound()
    return result[0]


def delete_article(request, article):
    article.enabled = False
    article.deleted_at = datetime.now()
    article.deleted_user = request.user
    article.board.article_count -= 1


def edit_article(request, article, subject, content):
    article_record = ArticleRecord(article)
    article.subject = subject
    article.change_content(content)
    request.dbsession.add(article_record)


def get_article_page(request, board, page):
    query = request.dbsession.query(Article).filter(Article.enabled == True).filter(Article.board == board).order_by(
        Article.uid.desc()).options(subqueryload(Article.user))
    start_idx = ARTICLE_PER_PAGE * (page - 1)
    end_idx = ARTICLE_PER_PAGE + start_idx
    return query[start_idx:end_idx]


def get_reply_page(request, article, page):
    query = request.dbsession.query(Reply).filter(Reply.enabled == True).filter(Reply.article == article).order_by(
        Reply.uid.desc()).options(subqueryload(Reply.user))
    start_idx = REPLY_PER_PAGE * (page - 1)
    end_idx = REPLY_PER_PAGE + start_idx
    return query[start_idx:end_idx]


def get_reply(request, reply_id):
    query = request.dbsession.query(Reply) \
        .filter(Reply.uid == reply_id) \
        .filter(Reply.enabled == True) \
        .options(subqueryload(Reply.user))
    result = query.all()
    if not result:
        raise PageNotFound()
    return result[0]


def delete_reply(request, reply):
    reply.enabled = False
    reply.deleted_at = datetime.now()
    reply.deleted_user = request.user
    reply.article.reply_count -= 1


def edit_reply(request, reply, content):
    reply_record = ReplyRecord(reply)
    reply.content = linkify(content, parse_email=True)
    request.dbsession.add(reply_record)


def create_article(request, board, subject, content):
    return Article(board, request.user, subject, content)


def create_reply(request, article, content):
    return Reply(article, request.user, content)