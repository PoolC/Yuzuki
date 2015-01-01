from helper.resource import YuzukiResource


class Hello(YuzukiResource):
    isLeaf = True

    def render_GET(self, request):
        return "Hello, World!"