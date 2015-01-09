from helper.resource import YuzukiResource
from helper.template import render_template


class About(YuzukiResource):
    isLeaf = True

    def render_GET(self, request):
        return render_template("about.html", request)