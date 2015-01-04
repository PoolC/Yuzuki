from helper.resource import YuzukiResource

class Index(YuzukiResource):
    def __init__(self):
        YuzukiResource.__init__(self)

    def render_GET(self, request):
        # TODO: index page
        return self.render_template("index.html", request)