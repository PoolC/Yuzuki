from helper.resource import YuzukiResource


class Hello(YuzukiResource):
    def render_GET(self, request):
        return "Hello, World!"