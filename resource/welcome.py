from helper.resource import YuzukiResource


class Welcome(YuzukiResource):
    isLeaf = True

    def render_GET(self, request):
        return self.render_template("welcome.html", request)