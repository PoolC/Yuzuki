from twisted.web.static import File

from resource.index import Index
from resource.api import Api
from resource.hello import Hello
from resource.login import Login
from resource.logout import Logout
from resource.register import Register

ROUTE = {
    "": Index(),
    "api": Api(),
    "login": Login(),
    "logout": Logout(),
    "register": Register(),
    "favicon.ico": File("static/img/favicon.ico"),
    "hello": Hello(),
}