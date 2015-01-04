from helper.resource import YuzukiResource
from model.user import User


class Register(YuzukiResource):
    def __init__(self):
        YuzukiResource.__init__(self)

    def render_GET(self, request):
        # TODO: show register page
        pass

    def render_POST(self, request):
        # TODO: register user
        pass