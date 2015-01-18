# -*- coding: utf-8 -*-
from twisted.web.resource import Resource
from twisted.web.server import NOT_DONE_YET

from exception import Unauthorized, Forbidden
from helper.permission import is_anybody


class YuzukiResource(Resource):
    def render(self, request):
        request.initialize(self)
        # TODO: auto login
        result = Resource.render(self, request)
        if result == NOT_DONE_YET:
            return result
        request.finalize()
        return result.encode("UTF-8")


def need_admin_permission(f):
    def _render_wrapper(resource, request):
        if not request.user:
            raise Unauthorized()
        if not request.user.is_admin:
            raise Forbidden()
        else:
            return f(resource, request)

    return _render_wrapper


def need_anybody_permission(f):
    def _render_wrapper(resource, request):
        if request.user and is_anybody(request):
            return f(resource, request)
        else:
            raise Unauthorized()

    return _render_wrapper
