from twisted.web.static import File

from resource.hello import Hello

ROUTE = {
    "": Hello(),
    "favicon.ico": File("static/img/favicon.ico"),
    "hello": Hello(),
}