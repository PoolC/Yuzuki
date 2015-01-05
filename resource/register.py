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
        username = request.get_argument("username")
        nickname = request.get_argument("nickname")
        password = request.get_argument("password")
        pd_realname = request.get_argument("pd_realname")
        pd_email = request.get_argument("pd_email")
        pd_address = request.get_argument("pd_address")
        pd_phone = request.get_argument("pd_phone")
        pd_bunryu = request.get_argument("pd_bunryu")
        pd_bio = request.get_argument("pd_bio")
        new_user = User(username, nickname, password, pd_realname, pd_email, pd_address, pd_phone, pd_bunryu, pd_bio)
        request.dbsession.add(new_user)
        request.dbsession.commit()
