# -*- coding: utf-8 -*-
from jinja2 import nodes, Markup
from jinja2.ext import Extension
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