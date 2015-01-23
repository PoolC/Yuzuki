# -*- coding: utf-8 -*-
from helper.resource import YuzukiResource
from helper.template import render_template
from localization import SITE_DESCRIPTION, SITE_INDEX


class Index(YuzukiResource):
    def render_GET(self, request):
        context = {"SITE_DESCRIPTION": SITE_DESCRIPTION}
        return render_template(SITE_INDEX, request, context)
