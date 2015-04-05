# -*- coding: utf-8 -*-

from twisted.internet import reactor, threads
from twisted.web.server import NOT_DONE_YET

from helper.resource import YuzukiResource


class Upload(YuzukiResource):
    def render_GET(self, request):
        return """
        <html>
        <head>
        <meta charset="utf-8"/>
        </head>
        <body>
        <form method="post" enctype="multipart/form-data">
        <input name="foo" type="file"/>
        <input type="submit" />
        </form>
        </body>
        </html>
"""

    def render_POST(self, request):
        fd = open("upload/foo", "wb")
        d = threads.deferToThread(self.write, fd, request)
        d.addCallback(self.finish, request)
        #reactor.call(d)
        return NOT_DONE_YET

    def write(self, fd, request):
        print "foo"
        fd.write(request.args["foo"][0])
        fd.close()

    def finish(self, result, request):
        print "bar"
        request.write("hey")
        request.finish()
