from twisted.web.resource import Resource


class Hello(Resource):
    isLeaf = True

    def render_GET(self, request):
        return "Hello, World!"