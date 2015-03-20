# -*- coding: utf-8 -*-
from exception import BadRequest
from helper.model_control import get_not_anybody_user
from helper.resource import YuzukiResource, need_admin_permission
from helper.template import render_template
from model.group import Group
from model.user import User


class Admin(YuzukiResource):
    isLeaf = False

    def __init__(self):
        YuzukiResource.__init__(self)
        self.putChild("approve", UserApprove())

    @need_admin_permission
    def render_GET(self, request):
        return "Hello"


class UserApprove(YuzukiResource):
    @need_admin_permission
    def render_GET(self, request):
        users = get_not_anybody_user(request)
        context = {"users": users}
        return render_template("admin_approve.html", request, context)

    @need_admin_permission
    def render_POST(self, request):
        user_id = request.get_argument_int("user_id")
        query = request.dbsession.query(User).filter(User.uid == user_id)
        result = query.all()
        if not result:
            raise BadRequest()
        user = result[0]
        query = request.dbsession.query(Group).filter(Group.name == "anybody")
        anybody = query.one()
        anybody.users.append(user)
        request.dbsession.commit()
        request.redirect("/admin/approve")
        return "redirect"
