# -*- coding: utf-8 -*-
import socket

hostname = socket.gethostname()

if hostname == "poolc":
    SITE_NAME = "PoolC"
    SITE_FAVICON = "static/img/favicon_poolc.png"

elif hostname == "ndm":
    SITE_NAME = "NDM"
    SITE_FAVICON = "static/img/favicon_ndm.png"
else:
    SITE_NAME = u"developing"
    SITE_FAVICON = "static/img/favicon_poolc.png"
