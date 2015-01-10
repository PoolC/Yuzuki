# -*- coding: utf-8 -*-
from twisted.web.http import BAD_REQUEST, UNAUTHORIZED, NOT_FOUND


class YuzukiException(Exception):
    """
    parent of all Yuzuki level defined exception
    """
    pass


class BadRequest(YuzukiException):
    status = BAD_REQUEST
    message = u"올바르지 않은 요청입니다."


class MissingArgument(BadRequest):
    pass


class DuplicateArgumentGiven(BadRequest):
    pass


class BadArgument(BadRequest):
    pass


class Unauthorized(YuzukiException):
    status = UNAUTHORIZED
    message = u"접근할 권한이 없습니다."


class PageNotFound(YuzukiException):
    status = NOT_FOUND
    message = u"페이지를 찾을 수 없습니다."