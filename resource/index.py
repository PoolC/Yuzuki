# -*- coding: utf-8 -*-
from StringIO import StringIO

from helper.resource import YuzukiResource
from helper.template import render_template
from config.config import SITE_DESCRIPTION
from helper.content import md


class Index(YuzukiResource):
    def render_GET(self, request):
        content = StringIO()
        with open("page/index") as f:
            md.convertFile(f, content, "utf-8")
            context = {
                "site_description": SITE_DESCRIPTION,
                "content": content.getvalue().decode("utf-8"),
                "is_index": True,
            }
        return render_template("page.html", request, context)
