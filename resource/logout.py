from twisted.web.http import UNAUTHORIZED

from helper.resource import YuzukiResource
from model.user import User


class Logout(YuzukiResource):
    def __init__(self):
        YuzukiResource.__init__(self)

    def render_GET(self, request):
        return self.logout(request)

    def render_POST(self, request):
        return self.logout(request)

    def logout(self, request):
        request.log_user_out()
        # TODO: reset auto login status
        request.redirect("/")
        return "logged out"