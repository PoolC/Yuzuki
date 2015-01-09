# -*- coding: utf-8 -*-
from markdown import Markdown

markdown_extension_list = [
    "extra",
    "admonition",
    "codehilite(css_class=highlight)",
    "nl2br",
    "sane_lists",
    "toc",
    "wikilinks",
]
md = Markdown(extensions=markdown_extension_list)


def markdown_convert(source):
    return md.convert(source)