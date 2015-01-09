from helper.resource import YuzukiResource


class Logout(YuzukiResource):
    def render_GET(self, request):
        return self.logout(request)

    def render_POST(self, request):
        return self.logout(request)

    def logout(self, request):
        request.log_user_out()
        # TODO: reset auto login status
        request.redirect("/")
        return "logged out"