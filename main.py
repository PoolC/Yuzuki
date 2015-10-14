# -*- coding: utf-8 -*-
import logging
import os
logger = logging.getLogger()
if not os.path.exists("log"):
    os.mkdir("log")

from twisted.internet import reactor, endpoints

from helper.site import YuzukiSite
from helper.resource import YuzukiResource
from route import ROUTE


class Main(YuzukiResource):
    isLeaf = False

    def __init__(self):
        YuzukiResource.__init__(self)
        for path in ROUTE:
            self.putChild(path, ROUTE[path])

logging.getLogger().info("Yuzuki started")
endpoints.serverFromString(reactor, "tcp:8080").listen(YuzukiSite(Main()))
reactor.run()
