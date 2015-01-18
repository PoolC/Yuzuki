# -*- coding: utf-8 -*-
import logging

from twisted.internet import reactor, endpoints
from twisted.web.resource import NoResource

from helper.site import YuzukiSite
from helper.resource import YuzukiResource
from resource.util import PageNotFound
from route import ROUTE


class Main(YuzukiResource):
    isLeaf = False

    def __init__(self):
        YuzukiResource.__init__(self)
        for path in ROUTE:
            self.putChild(path, ROUTE[path])
        self.page_not_found = PageNotFound()

    def getChildWithDefault(self, path, request):
        resource = YuzukiResource.getChildWithDefault(self, path, request)
        request.logger = logging.getLogger(resource.__class__.__module__)
        log_str = request.method + " " + request.get_path_and_query()
        if request.user:
            log_str += " " + request.user.username
        request.logger.info(log_str)
        if isinstance(resource, NoResource):
            return self.page_not_found
        return resource


endpoints.serverFromString(reactor, "tcp:8080").listen(YuzukiSite(Main()))
reactor.run()
