# -*- coding: utf-8 -*-
from twisted.web.http import UNAUTHORIZED

from helper.resource import YuzukiResource
from model.user import User


class Login(YuzukiResource):
    def __init__(self):
        YuzukiResource.__init__(self)

    def render_GET(self, request):
        return self.render_login_page(request, False)

    def render_POST(self, request):
        username = request.get_argument("username")
        password = request.get_argument("password")
        remember_me = request.get_argument("remember_me", None)
        query = request.dbsession.query(User).filter(User.username == username)
        result = query.all()
        if result:
            user = result[0]
            if user.check_password(password):
                request.log_user_in(user)
                # TODO: remember me feature
                redirect = request.get_argument("redirect", "/")
                request.redirect(redirect)
                return "logged in"
            else:
                request.setResponseCode(UNAUTHORIZED)
                return self.render_login_page(request, True)
        else:
            request.setResponseCode(UNAUTHORIZED)
            return self.render_login_page(request, True)

    def render_login_page(self, request, error):
        redirect = request.get_argument("redirect", "")
        context = {
            "redirect": redirect
        }
        if error:
            context["error"] = "ID나 비밀번호가 잘못되었습니다."
        return self.render_template("login.html", request, context)