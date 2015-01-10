# -*- coding: utf-8 -*-
from twisted.web.http import FORBIDDEN
from twisted.web.resource import Resource

from helper.template import generate_error_message


class YuzukiResource(Resource):
    def render(self, request):
        request.initialize(self)
        # TODO: auto login
        result = Resource.render(self, request)
        request.finalize()
        return result.encode("UTF-8")


def need_admin_permission(f):
    def _render_wrapper(resource, request):
        if request.user and request.user.is_admin:
            return f(resource, request)
        else:
            request.setResponseCode(FORBIDDEN)
            return generate_error_message(request, FORBIDDEN, u"관리자만 볼 수 있는 페이지입니다.")

    return _render_wrapper