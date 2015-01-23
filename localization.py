# -*- coding: utf-8 -*-
import socket

hostname = socket.gethostname()

if hostname == "poolc":
    SITE_NAME = "PoolC"
    SITE_ABOUT = "about_poolc.html"
    SITE_INDEX = "index_poolc.html"
    SITE_FAVICON = "static/img/favicon_poolc.png"
    SITE_DESCRIPTION = u"연세대학교 공학대학 프로그래밍 학술동아리 PoolC 홈페이지입니다."

elif hostname == "ndm":
    SITE_NAME = "NDM"
    SITE_ABOUT = "about_ndm.html"
    SITE_INDEX = "index_ndm.html"
    SITE_FAVICON = "static/img/favicon_ndm.png"
    SITE_DESCRIPTION = u"Nexon의 게임개발 동아리 지원사업 Nexon Dream Members의 홈페이지입니다."

else:
    SITE_NAME = u"developing"
    SITE_ABOUT = "about_default.html"
    SITE_INDEX = "index_poolc.html"
    SITE_FAVICON = "static/img/favicon_poolc.png"
    SITE_DESCRIPTION = "no site description"
