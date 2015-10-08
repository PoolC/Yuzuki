# -*- coding: utf-8 -*-
from helper.resource import YuzukiResource
from helper.template import render_template
from localization import SITE_DESCRIPTION, SITE_INDEX
from helper.content import md
from StringIO import StringIO

class Index(YuzukiResource):
    def render_GET(self, request):
        content = StringIO()
        with open("page/index") as f:
            md.convertFile(f, content, "utf-8")
            context = {
                "SITE_DESCRIPTION": SITE_DESCRIPTION,
                "content": content.getvalue().decode("utf-8"),
            }
            print context
        return render_template("page.html", request, context)
