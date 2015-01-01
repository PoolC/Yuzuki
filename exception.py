# -*- coding: utf-8 -*-

class NodokaException(Exception):
    """
    parent of all Nodoka level defined exception
    """
    pass

class MissingArgument(NodokaException):
    status = 400
    
    def __init__(self, key):
        NodokaException.__init__(self, "Missing argument key is \"%s\"." % key)

class DuplicateArgumentGiven(NodokaException):
    status = 400
    
    def __init__(self, key):
        NodokaException.__init__(self, "Duplicate key \"%s\" is given as argument" % key)