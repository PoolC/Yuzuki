# -*- coding: utf-8 -*-
from twisted.web.static import File

from localization import SITE_FAVICON
from resource.admin import Admin
from resource.article import ArticleParent
from resource.board import Board
from resource.chat import Chat
from resource.hello import Hello
from resource.index import Index
from resource.login import Login
from resource.logout import Logout
from resource.new import New
from resource.page import Page
from resource.profile import Profile
from resource.register import Register
from resource.reply import ReplyParent
from resource.search import Search
from resource.welcome import Welcome

ROUTE = {
    "": Index(),
    "admin": Admin(),
    "article": ArticleParent(),
    "board": Board(),
    "chat": Chat(),
    "hello": Hello(),
    "login": Login(),
    "logout": Logout(),
    "favicon.ico": File(SITE_FAVICON),
    "new": New(),
    "profile": Profile(),
    "page": Page(),
    "register": Register(),
    "reply": ReplyParent(),
    "robots.txt": File("static/etc/robots.txt"),
    "static": File("static"),
    "search": Search(),
    "welcome": Welcome(),
}
