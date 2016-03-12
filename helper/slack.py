# -*- coding: utf-8 -*-
import json
import urllib

from bleach import clean
from twisted.internet import reactor
from twisted.internet.ssl import ClientContextFactory
from twisted.web.client import Agent, readBody
from twisted.web.http_headers import Headers

from config.config import SLACK_NOTI_CHANNEL, SLACK_POST_INFO,\
    SLACK_NOTI_TARGET_BOARDS

SLACK_CHAT_POST_MESSAGE_URL = "https://slack.com/api/chat.postMessage"


class WebClientContextFactory(ClientContextFactory):
    def getContext(self, hostname, port):
        return ClientContextFactory.getContext(self)

contextFactory = WebClientContextFactory()
agent = Agent(reactor, contextFactory)


def post_messages_to_subscribers(request, subscribers, text, actor, title,
                                 content, url):
    for subscriber in subscribers:
        if subscriber == actor:
            continue
        if subscriber.slack_id:
            post_message(request, text, actor.nickname,
                         "@{0}".format(subscriber.slack_id), title,
                         content, url)


def post_new_article_message(request, article, article_view_url):
    if article.board.repr not in SLACK_NOTI_TARGET_BOARDS:
        return
    content = clean(article.compiled_content, tags=[], strip=True)
    if len(content) > 30:
        content = content[:27] + "..."
    return post_message(
        request,
        u"%s에 새 글이 등록되었습니다." % article.board.repr,
        article.user.nickname,
        SLACK_NOTI_CHANNEL,
        article.subject,
        content,
        article_view_url
    )


def post_message(request, text, actor, channel, title, content, article_url):
    article_link = "{0}://{1}{2}".format(request.getProto(),
                                         request.getRequestHostname(),
                                         article_url)
    params = {
        "text": text,
        "channel": channel,
    }
    params.update(SLACK_POST_INFO)
    attachments = list()
    attachments.append({
        "title": title,
        "title_link": article_link,
        "text": content,
        "author_name": actor,
    })
    params["attachments"] = json.dumps(attachments)
    params = {key: params[key].encode("utf-8")
              if type(params[key]) in (unicode, str) else params[key]
              for key in params}
    get_args = urllib.urlencode(params)

    d = agent.request(
        "GET",
        "https://slack.com/api/chat.postMessage?" + get_args,
        Headers({"User-Agent": ["Twisted Web Server Slack Notify"]}),
        None
    )
    d.addBoth(slack_callback, request)


def slack_callback(resp, request):
    d = readBody(resp)
    d.addCallback(slack_resp, request)


def slack_resp(resp_body, request):
    response = json.loads(resp_body)
    if not response["ok"]:
        request.logger.error("Slack post message error : %s",
                             response["error"])
