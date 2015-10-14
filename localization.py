# -*- coding: utf-8 -*-
import socket

hostname = socket.gethostname()

if hostname == "poolc":
    SITE_NAME = "PoolC"
elif hostname == "ndm":
    SITE_NAME = "NDM"
else:
    SITE_NAME = u"developing"
