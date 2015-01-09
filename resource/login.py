# -*- coding: utf-8 -*-
from twisted.web.http import UNAUTHORIZED

from helper.resource import YuzukiResource
from helper.template import render_template
from model.user import User


class Login(YuzukiResource):
    INVALID_CREDENTIAL = u"ID나 비밀번호가 잘못되었습니다."
    BLOCKED_USER = u"차단된 계정입니다."

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
            if user.is_blocked:
                return self.render_login_page(request, self.BLOCKED_USER)
            if user.check_password(password):
                request.log_user_in(user)
                # TODO: remember me feature
                redirect = request.get_argument("redirect", "/")
                request.redirect(redirect)
                return "logged in"
            else:
                request.setResponseCode(UNAUTHORIZED)
                return self.render_login_page(request, self.INVALID_CREDENTIAL)
        else:
            request.setResponseCode(UNAUTHORIZED)
            return self.render_login_page(request, self.INVALID_CREDENTIAL)

    def render_login_page(self, request, err):
        redirect = request.get_argument("redirect", "/")
        context = {
            "redirect": redirect
        }
        if err:
            context["err"] = err
        return render_template("login.html", request, context)