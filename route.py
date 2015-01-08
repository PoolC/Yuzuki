from twisted.web.static import File

from resource.index import Index
from resource.article import ArticleParent
from resource.reply import ReplyParent
from resource.about import About
from resource.board import BoardView
from resource.hello import Hello
from resource.login import Login
from resource.logout import Logout
from resource.register import Register
from resource.welcome import Welcome
from resource.profile import Profile

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