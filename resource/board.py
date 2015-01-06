from helper.resource import YuzukiResource

class Board(YuzukiResource):
    def render_GET(self, request):
        return "Hello, World!"