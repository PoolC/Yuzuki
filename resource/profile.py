# -*- coding: utf-8 -*-
from bleach import linkify
from twisted.web.http import UNAUTHORIZED

from helper.md_ext import markdown_convert
from helper.pbkdf2 import pbkdf2
from helper.resource import YuzukiResource
from helper.template import render_template, generate_error_message
from model.user import User


class Profile(YuzukiResource):
    isLeaf = False

    def __init__(self):
        YuzukiResource.__init__(self)
        self.putChild("view", ProfileView())
        self.putChild("edit", ProfileEdit())


class ProfileView(YuzukiResource):
    def render_GET(self, request):
        if not request.user:
            request.setResponseCode(UNAUTHORIZED)
            return generate_error_message(request, UNAUTHORIZED, u"로그인이 필요합니다.")
        else:
            context = {"user": request.user}
            return render_template("profile_view.html", request, context)


class ProfileEdit(YuzukiResource):
    def render_GET(self, request):
        if not request.user:
            request.setResponseCode(UNAUTHORIZED)
            return generate_error_message(request, UNAUTHORIZED, u"로그인이 필요합니다.")
        else:
            return render_template("profile_edit.html", request)

    def render_POST(self, request):
        if not request.user:
            request.setResponseCode(UNAUTHORIZED)
            return generate_error_message(request, UNAUTHORIZED, u"로그인이 필요합니다.")
        else:
            nickname = request.get_argument("nickname") or None
            password = request.get_argument("password") or None
            pd_realname = request.get_argument("pd_realname") or None
            pd_email = request.get_argument("pd_email") or None
            pd_address = request.get_argument("pd_address") or None
            pd_phone = request.get_argument("pd_phone") or None
            pd_bio = request.get_argument("pd_bio") or None

            query = request.dbsession.query(User).filter(User.nickname == nickname)
            if request.dbsession.query(query.exists()).scalar():
                err = u"이미 사용되고 있는 별명입니다."
                context = {"err": err}
                return render_template("profile_edit.html", request, context)
            else:
                if nickname:
                    request.user.nickname = nickname
                if password:
                    request.user.password = pbkdf2(password)
                if pd_realname:
                    request.user.pd_realname = pd_realname
                if pd_email:
                    request.user.pd_email = pd_email
                if pd_address:
                    request.user.pd_address = pd_address
                if pd_phone:
                    request.user.pd_phone = pd_phone
                if pd_bio:
                    request.user.pd_bio = linkify(markdown_convert(pd_bio), parse_email=True)
                request.dbsession.commit()
                request.redirect("/profile/view")
                return "profile edit success"