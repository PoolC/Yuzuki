# -*- coding: utf-8 -*-
import logging

from twisted.web.resource import NoResource, Resource
from twisted.web.server import NOT_DONE_YET

from exception import PageNotFound, Unauthorized
from helper.permission import is_anybody


class YuzukiResource(Resource):
    def render(self, request):
        request.initialize(self)
        result = Resource.render(self, request)
        if result == NOT_DONE_YET:
            return result
        request.finalize()
        return result.encode("UTF-8")

    def getChildWithDefault(self, path, request):
        resource = Resource.getChildWithDefault(self, path, request)

        request.logger = logging.getLogger(resource.__class__.__module__)
        log_str = request.method + " " + request.path
        if request.user:
            log_str += " " + request.user.username
        request.logger.info(log_str)

        if isinstance(resource, NoResource):
            raise PageNotFound()

        return resource


def need_admin_permission(f):
    def _render_wrapper(resource, request):
        if not request.user or not request.user.is_admin:
            raise Unauthorized()
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
