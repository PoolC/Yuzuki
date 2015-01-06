from helper.resource import YuzukiResource


class About(YuzukiResource):
    isLeaf = True

    def render_GET(self, request):
        return "Hello, World!"