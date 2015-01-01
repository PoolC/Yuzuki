# -*- coding: utf-8 -*-
from twisted.web.server import Site, Session

from helper.request import YuzukiRequest

class YuzukiSession(Session):
    sessionTimeout = 7200 # two hours

class YuzukiSite(Site):
    def __init__(self, resource, *args, **kwargs):
        Site.__init__(self, resource, *args, **kwargs)
        self.requestFactory = YuzukiRequest
        self.sessionFactory = YuzukiSession