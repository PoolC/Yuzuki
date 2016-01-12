# -*- coding: utf-8 -*-
from helper.resource import YuzukiResource
from helper.template import render_template
from config.config import SITE_DESCRIPTION
from helper.content import markdown_convert_file


class Index(YuzukiResource):
    def render_GET(self, request):
        with open("page/index") as f:
            context = {
                "site_description": SITE_DESCRIPTION,
                "content": markdown_convert_file(f),
                "is_index": True,
            }
        return render_template("page.html", request, context)
