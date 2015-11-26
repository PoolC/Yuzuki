# -*- coding: utf-8 -*-
from config import SLACK_NOTI_CHANNEL, SLACK_POST_INFO, SLACK_NOTI_TARGET_BOARDS, logger
import json
import threading
from bleach import clean

SLACK_CHAT_POST_MESSAGE_URL = "https://slack.com/api/chat.postMessage"

def post_message(request, article, article_view_url):
    if article.board.repr not in SLACK_NOTI_TARGET_BOARDS:
        return
    article_link = request.getProto() + "://" + request.getHost() + article_view_url
    content = clean(article.compiled_content, tags=[], strip=True)
    if len(content) > 30:
        content = content[:27] + '...'
    params = {
        'text': u"%s에 새 글이 등록되었습니다." % article.board.repr,
        'channel': SLACK_NOTI_CHANNEL,
    }
    params.update(SLACK_POST_INFO)
    attachments = list()
    attachments.append({
        'title': article.subject,
        'title_link': article_link,
        'text': content,
        'author_name': article.author.nickname,
    })
    params['attachments'] = json.dumps(attachments)

    thread = threading.Thread(target=post_message_inner, args=(params,))
    thread.start()

def post_message_inner(params):
    res = requests.get(SLACK_CHAT_POST_MESSAGE_URL, params=params)
    response = json.loads(res.text)
    if not response["ok"]:
        logger.error("Slack post message error : %s", response["error"])
