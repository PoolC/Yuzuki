from helper.resource import YuzukiResource
class BoardView(YuzukiResource):

    def render_GET(self, request):
        return "Hello, World!"