from twisted.web.static import File

from resource.hello import Hello
from resource.login import Login
from resource.register import Register

ROUTE = {
    "": Hello(),
    "login": Login(),
    "register": Register(),
    "favicon.ico": File("static/img/favicon.ico"),
    "hello": Hello(),
}