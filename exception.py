# -*- coding: utf-8 -*-
from twisted.web.http import BAD_REQUEST, UNAUTHORIZED, NOT_FOUND, RESPONSES


class YuzukiException(Exception):
    """
    parent of all Yuzuki level defined exception
    """
    pass


class BadRequest(YuzukiException):
    status = BAD_REQUEST
    message = u"올바르지 않은 요청입니다."


class MissingArgument(BadRequest):
    def __init__(self, key):
        self.log = u"Missing argument key is \"%s\"." % key


class DuplicateArgumentGiven(BadRequest):
    def __init__(self, key):
        self.log = u"Duplicate key \"%s\" is given as argument" % key


class BadArgument(BadRequest):
    def __init__(self, key, value):
        self.log = u"Bad Argument \"%s=%s\"" % (key, value)


class Unauthorized(YuzukiException):
    status = UNAUTHORIZED
    message = u"접근할 권한이 없습니다."

    def __init__(self, log=None):
        self.log = log if log else RESPONSES[self.status]


class PageNotFound(YuzukiException):
    status = NOT_FOUND
    message = u"페이지를 찾을 수 없습니다."
    log = RESPONSES[NOT_FOUND]