from helper.resource import YuzukiResource
from helper.template import render_template

class Index(YuzukiResource):
    def __init__(self):
        YuzukiResource.__init__(self)

    def render_GET(self, request):
        # TODO: index page
        return render_template("index.html", request)