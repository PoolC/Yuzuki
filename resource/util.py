# -*- coding: utf-8 -*-
from twisted.web.http import NOT_FOUND

from helper.resource import YuzukiResource


class PageNotFound(YuzukiResource):
    def render_GET(self, request):
        request.setResponseCode(NOT_FOUND)
        return self.generate_error_message(request,
                                           NOT_FOUND,
                                           "Not Found",
                                           u"페이지를 찾을 수 없습니다")