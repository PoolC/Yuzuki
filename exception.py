# -*- coding: utf-8 -*-
from twisted.web.http import BAD_REQUEST, UNAUTHORIZED, NOT_FOUND, FORBIDDEN


class YuzukiException(Exception):
    """
    parent of all Yuzuki level defined exception
    """
    pass


class BadRequest(YuzukiException):
    status = BAD_REQUEST
    message = u"올바르지 않은 요청입니다."


class Unauthorized(YuzukiException):
    status = UNAUTHORIZED
    message = u"로그인 하지 않았거나 가입이 승인된 사용자가 아닙니다."


class PageNotFound(YuzukiException):
    status = NOT_FOUND
    message = u"페이지를 찾을 수 없습니다."


class Forbidden(YuzukiException):
    status = FORBIDDEN
    message = u"접근이 금지되어있습니다."
