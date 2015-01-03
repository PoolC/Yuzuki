from helper.resource import YuzukiResource

class Api(YuzukiResource):
    def __init__(self):
        YuzukiResource.__init__(self)

    def render_GET(self, request):
        # TODO: index page
        return "Hello, World!"