# -*- coding: utf-8 -*-
from markdown import Markdown

markdown_extension_list = [
    "abbr",
    "attr_list",
    "def_list",
    "fenced_code",
    "tables",
    "smart_strong",
    "admonition",
    "codehilite",
    "nl2br",
    "sane_lists",
    "toc",
    "wikilinks",
]
md = Markdown(extensions=markdown_extension_list)


def markdown_convert(source):
    return md.convert(source)
