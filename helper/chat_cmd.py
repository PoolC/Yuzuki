# -*- coding: utf-8 -*-
import re

from model.user import User
from helper.request import YuzukiRequest
from helper.model_control import create_chat

dbsession = YuzukiRequest.dbsession
query = dbsession.query(User).filter(User.username == "chat_system")
chat_system = query.all()[0]


class _man():
    def __init__(self, processor_map):
        self.processor_map = processor_map
        self.usage = u"(사용법 /man [" + ", ".join(processor_map.keys()) + "])"
        self.man = u"명령어의 사용법을 알려줍니다. " + self.usage

    def process(self, request, cmd_args):
        if len(cmd_args) > 1:
            return None, None, u"인자의 수가 올바르지 않습니다. " + self.usage
        if len(cmd_args) == 0:
            return None, None, self.man
        if cmd_args[0] not in self.processor_map:
            return None, None, u"그런 명령어는 존재하지 않습니다. /man 을 참조하세요."
        processor = self.processor_map[cmd_args[0]]
        return None, None, processor.man


class change_color():
    def __init__(self):
        self.usage = u"(사용법: /color COFFEE)"
        self.man = u"메시지의 색상을 변경합니다. 6자리 16진수로 웹 코드를 사용합니다. " + self.usage

    def process(self, request, cmd_arg):
        color = cmd_arg
        if not re.match(r"^[0-9a-fA-F]{6}$", color):
            return None, None, u"올바른 색상 코드가 아닙니다. 6자리 16진수로 입력하세요. " + self.usage
        request.user.chat_color = color.lower()
        return request.user, u"색상을 #%s로 변경합니다" % color.lower(), None


_chat_cmd_map = {
    "color": change_color(),
}

_man_proc = _man(_chat_cmd_map)
_chat_cmd_map["man"] = _man_proc


def process_cmd(request, content):
    cmd_parts = content.split(" ")
    cmd_name = cmd_parts[0][1:]
    cmd_arg = content[len(cmd_name) + 2:]
    processor = _chat_cmd_map[cmd_name] if cmd_name in _chat_cmd_map else None
    if not processor:
        return None, u"그런 명령어는 존재하지 않습니다. /man 을 참조하세요."
    speaker, message, err = processor.process(request, cmd_arg)
    if not err:
        chat = create_chat(request, message, speaker)
        return chat, None
    else:
        return None, err
