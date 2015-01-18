# -*- coding: utf-8 -*-
from helper.resource import YuzukiResource


class Logout(YuzukiResource):
    def render_GET(self, request):
        return self.logout(request)

    def render_POST(self, request):
        return self.logout(request)

    def logout(self, request):
        request.log_user_out()
        request.remove_auto_login_cookie()
        request.redirect("/")
        return "logged out"
