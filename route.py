from twisted.web.static import File

from resource.about import About
from resource.article import ArticleParent
from resource.board import BoardView
from resource.hello import Hello
from resource.index import Index
from resource.login import Login
from resource.logout import Logout
from resource.profile import Profile
from resource.register import Register
from resource.reply import ReplyParent
from resource.welcome import Welcome

ROUTE = {
    "": Index(),
    "article": ArticleParent(),
    "reply": ReplyParent(),
    "about": About(),
    "board": BoardView(),
    "login": Login(),
    "logout": Logout(),
    "register": Register(),
    "favicon.ico": File("static/img/favicon.ico"),
    "static": File("static"),
    "hello": Hello(),
    "welcome": Welcome(),
    "profile": Profile(),
}