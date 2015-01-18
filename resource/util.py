# -*- coding: utf-8 -*-
from exception import PageNotFound as PageNotFoundException
from helper.resource import YuzukiResource


class PageNotFound(YuzukiResource):
    isLeaf = False

    def render_GET(self, request):
        raise PageNotFoundException()

    def render_POST(self, request):
        raise PageNotFoundException()

    def render_DELETE(self, request):
        raise PageNotFoundException()

    def getChildWithDefault(self, path, request):
        return self
