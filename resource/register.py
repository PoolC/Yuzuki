# -*- coding: utf-8 -*-
from helper.database import DatabaseHelper
from helper.resource import YuzukiResource
from model.user import User
from model.group import Group


class Register(YuzukiResource):
    def __init__(self):
        YuzukiResource.__init__(self)
        dbsession = DatabaseHelper.session()
        query = dbsession.query(Group).filter(Group.important == True)
        result = query.all()
        self.bunryu_groups = [(group.uid, group.name) for group in result]
        dbsession.close()

    def render_GET(self, request):
        context = {"group_meta": self.bunryu_groups}
        return self.render_template("register.html", request, context)

    def render_POST(self, request):
        username = request.get_argument("username") or None
        nickname = request.get_argument("nickname") or None
        password = request.get_argument("password") or None
        pd_realname = request.get_argument("pd_realname") or None
        pd_email = request.get_argument("pd_email") or None
        pd_address = request.get_argument("pd_address") or None
        pd_phone = request.get_argument("pd_phone") or None
        pd_bunryu = request.get_argument("pd_bunryu") or None
        pd_bio = request.get_argument("pd_bio") or None
        new_user = User(username, nickname, password, pd_realname, pd_email, pd_address, pd_phone, pd_bunryu, pd_bio)
        err = self.check_user_data_valid(request, new_user)
        if err == None:
            request.dbsession.add(new_user)
            request.dbsession.commit()
            request.redirect("/welcome")
            return "registered successfully"
        else:
            context = {
                "group_meta": self.bunryu_groups,
                "err": err,
            }
            return self.render_template("register.html", request, context)

    def check_user_data_valid(self, request, new_user):
        # empty value check
        if new_user.username == None:
            return u"ID는 비어있을 수 없습니다."
        if new_user.nickname == None:
            return u"별명은 비어있을 수 없습니다."
        if new_user.password == None:
            return u"비밀번호는 비어있을 수 없습니다."
        if new_user.pd_realname == None:
            return u"실명은 비어있을 수 없습니다."
        if new_user.pd_bunryu == None:
            return u"분류는 비어있을 수 없습니다."

        # duplicate value check
        user_query = request.dbsession.query(User)
        query = user_query.filter(User.username == new_user.username)
        if request.dbsession.query(query.exists()).scalar():
            return u"이미 사용되고 있는 ID입니다."
        query = user_query.filter(User.nickname == new_user.nickname)
        if request.dbsession.query(query.exists()).scalar():
            return u"이미 사용되고 있는 별명입니다."

        # bunryu existence check
        query = request.dbsession.query(Group).filter(Group.uid == new_user.pd_bunryu)
        if not request.dbsession.query(query.exists()).scalar():
            return u"존재하지 않는 분류 그룹입니다."

        # all green
        return None