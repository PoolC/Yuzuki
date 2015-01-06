from twisted.web.static import File

from resource.index import Index
from resource.about import About
from resource.api import Api
from resource.board import BoardView
from resource.hello import Hello
from resource.login import Login
from resource.logout import Logout
from resource.register import Register
from resource.welcome import Welcome

ROUTE = {
    "": Index(),
    "about": About(),
    "api": Api(),
    "board": BoardView(),
    "login": Login(),
    "logout": Logout(),
    "register": Register(),
    "favicon.ico": File("static/img/favicon.ico"),
    "static": File("static"),
    "hello": Hello(),
    "welcome": Welcome(),
}