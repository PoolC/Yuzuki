# -*- coding: utf-8 -*-

class YuzukiException(Exception):
    """
    parent of all Yuzuki level defined exception
    """
    pass


class MissingArgument(YuzukiException):
    status = 400

    def __init__(self, key):
        YuzukiException.__init__(self, "Missing argument key is \"%s\"." % key)


class DuplicateArgumentGiven(YuzukiException):
    status = 400

    def __init__(self, key):
        YuzukiException.__init__(self, "Duplicate key \"%s\" is given as argument" % key)


class BadArgument(YuzukiException):
    def __init__(self, key, value):
        YuzukiException.__init__(self, "Bad Argument \"%s=%s\"" % (key, value))