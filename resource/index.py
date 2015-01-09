# -*- coding: utf-8 -*-
from helper.resource import YuzukiResource
from helper.template import render_template


class Index(YuzukiResource):
    def render_GET(self, request):
        # TODO: index page
        return render_template("index.html", request)