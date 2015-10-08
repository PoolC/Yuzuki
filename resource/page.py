# -*- coding: utf-8 -*-
import os
from StringIO import StringIO

from exception import BadRequest, PageNotFound
from helper.content import md
from helper.resource import YuzukiResource
from helper.template import render_template


class Page(YuzukiResource):
    isLeaf = False

    def render_GET(self, request):
        if len(request.path.split("/")) != 3:
            raise BadRequest()
        name = request.path.split("/")[2]
        if not name:
            raise BadRequest()
        file_path = "page/%s" % name
        if not os.path.isfile(file_path):
            raise PageNotFound()
        with open(file_path) as f:
            content = StringIO()
            md.convertFile(f, content, "utf-8")
            context = {
                "content": content.getvalue(),
            }
            return render_template("page.html", request, context)

    def getChildWithDefault(self, path, request):
        if len(request.path.split("/")) != 3:
            raise BadRequest()
        return self
