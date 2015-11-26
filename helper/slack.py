# -*- coding: utf-8 -*-
import json
import StringIO
import urllib

from bleach import clean
from twisted.internet import reactor
from twisted.web.client import Agent, FileBodyProducer, readBody
from twisted.web.http_headers import Headers

from config import SLACK_NOTI_CHANNEL, SLACK_POST_INFO, SLACK_NOTI_TARGET_BOARDS, logger

SLACK_CHAT_POST_MESSAGE_URL = "https://slack.com/api/chat.postMessage"

agent = Agent(reactor)

def post_message(request, article, article_view_url):
    if article.board.repr not in SLACK_NOTI_TARGET_BOARDS:
        return
    article_link = request.getProto() + "://" + request.getHost() + article_view_url
    content = clean(article.compiled_content, tags=[], strip=True)
    if len(content) > 30:
        content = content[:27] + "..."
    params = {
        "text": u"%s에 새 글이 등록되었습니다." % article.board.repr,
        "channel": SLACK_NOTI_CHANNEL,
    }
    params.update(SLACK_POST_INFO)
    attachments = list()
    attachments.append({
        "title": article.subject,
        "title_link": article_link,
        "text": content,
        "author_name": article.author.nickname,
    })
    params["attachments"] = json.dumps(attachments)
    body = FileBodyProducer(StringIO.StringIO(urllib.urlencode(params)))

    d = agent.request(
        "POST",
        "https://slack.com/api/chat.postMessage",
        Headers({"User-Agent": ["Twisted Web Server Slack Notify"]}),
        body
    )
    d.addBoth(slack_callback)

def slack_callback(resp):
        d = readBody(resp)
        d.addCallback(slack_resp)

def slack_resp(resp_body):
    response = json.loads(resp_body)
    if not response["ok"]:
        logger.error("Slack post message error : %s", response["error"])
