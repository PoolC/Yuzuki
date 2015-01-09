# -*- coding: utf-8 -*-
from helper.resource import YuzukiResource
from helper.template import render_template


class About(YuzukiResource):
    def render_GET(self, request):
        return render_template("about.html", request)