import requests
from config import SLACK_POST_INFO, logger
import json
import threading
from bleach import clean

SLACK_CHAT_POST_MESSAGE_URL = "https://slack.com/api/chat.postMessage"

class SlackAttachment:
    def to_slack_attachment(self):
        return {}

class ArticleInfo(SlackAttachment):
    def __init__(self, article, url):
        self.title = article.subject
        self.url = url
        self.content = clean(article.compiled_content, tags=[], strip=True)
        if len(self.content) > 30:
            self.content = self.content[:27] + '...'
        self.author = article.user.nickname

    def to_slack_attachment(self):
        return {
            'title': self.title,
            'title_link': self.url,
            'text': self.content,
            'author_name': self.author,
        }

    def __repr__(self):
        return json.dumps(self.to_slack_attachment())

def post_message(channel, text, attachments = None):
    params = {
        'text': text,
        'channel': channel
    }
    params.update(SLACK_POST_INFO)

    if attachments:
        attachments_converted = [attachment.to_slack_attachment()
                                 if isinstance(attachment, SlackAttachment)
                                 else { 'text': str(attachment) }
                                 for attachment in attachments]
        params['attachments'] = json.dumps(attachments_converted)

    thread = threading.Thread(target=post_message_inner, args=(params,))
    thread.start()

def post_message_inner(params):
    res = requests.get(SLACK_CHAT_POST_MESSAGE_URL, params=params)
    response = json.loads(res.text)
    if not response["ok"]:
        logger.error("Slack post message error : %s", response["error"])
