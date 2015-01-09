# -*- coding: utf-8 -*-
import copy
from urllib import quote

from sqlalchemy.orm import subqueryload
from twisted.python.compat import intToBytes
from twisted.web.http import INTERNAL_SERVER_ERROR, BAD_REQUEST
from twisted.web.server import Request

from config import DEBUG
from exception import DuplicateArgumentGiven, MissingArgument, YuzukiException
from helper.database import DatabaseHelper
from helper.template import generate_error_message
from model.user import User


class NoArgument:
    pass


class YuzukiRequest(Request):
    def initialize(self, resource):
        """
        if you need to do something just before or just after a request is initialized,
        write it here
        """
        self._initial_session = copy.deepcopy(self.yzk_session)

    def finalize(self):
        """
        if you need to do something just before or just after a request is finished,
        write it here
        """
        if hasattr(self, "_dbsession"):
            self._dbsession.close()
        if self._initial_session != self.yzk_session:
            self.session.redis_sync()

    @property
    def dbsession(self):
        if not hasattr(self, "_dbsession"):
            self._dbsession = DatabaseHelper.session()
        return self._dbsession

    @property
    def yzk_session(self):
        twisted_session = self.getSession()
        if not hasattr(twisted_session, "yuzuki_session_data"):
            twisted_session.yuzuki_session_data = dict()
        return twisted_session.yuzuki_session_data

    def log_user_in(self, user):
        self.yzk_session["login_user"] = user.uid

    def log_user_out(self):
        if "login_user" in self.yzk_session:
            del self.yzk_session["login_user"]

    def _is_user_logged_in(self):
        return "login_user" in self.yzk_session

    @property
    def user(self):
        if hasattr(self, "_user"):
            return self._user
        user_id = self.yzk_session["login_user"] if self._is_user_logged_in() else None
        if not user_id:
            return None
        else:
            query = self.dbsession.query(User).filter(User.uid == user_id).options(subqueryload(User.groups))
            result = query.all()
            user = result[0]
            self._user = user
            return user

    def get_argument(self, key, default=NoArgument):
        args = self.args.get(key, None)
        if not args:
            if default == NoArgument:
                raise MissingArgument(key)
            else:
                return default
        else:
            if len(args) == 1:
                return unicode(args[0], "utf8")
            else:
                raise DuplicateArgumentGiven(key)

    def get_path_and_query(self):
        result = self.path
        if self.args:
            result += "?"
            for i, key in enumerate(self.args):
                for j, value in enumerate(self.args[key]):
                    result += key
                    result += "="
                    result += quote(value, "")
                    if not (i == len(self.args) - 1 and j == len(self.args[key]) - 1):
                        result += "&"
        return result

    def processingFailed(self, reason):
        if DEBUG:
            return Request.processingFailed(self, reason)
        else:
            if issubclass(reason.type, YuzukiException):
                self.logger.warning(reason)
                self.setResponseCode(BAD_REQUEST)
                body = generate_error_message(self, BAD_REQUEST, u"올바르지 않은 요청입니다.")
            else:
                self.logger.error(reason)
                self.setResponseCode(INTERNAL_SERVER_ERROR)
                body = generate_error_message(self, INTERNAL_SERVER_ERROR, u"서버 에러가 발생하였습니다.")
            body = body.encode("UTF-8")
            self.setHeader(b'content-type', b"text/html")
            self.setHeader(b'content-length', intToBytes(len(body)))
            self.write(body)
            self.finish()
            return reason

    def redirect(self, url):
        if isinstance(url, unicode):
            url = url.encode("UTF-8")
        Request.redirect(self, url)