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

def do_markdown(source):
    return md.convert(source)

class MarkdownExtension(Extension):
    # a set of names that trigger the extension.
    tags = set(['markdown'])
    
    def parse(self, parser):
        lineno = parser.stream.next().lineno
        #no args for this extension
        args = tuple()
        body = parser.parse_statements(['name:endmarkdown'], drop_needle=True)
        call = self.call_method('_markdown_support', args)
        return nodes.CallBlock(call, list(), list(), body).set_lineno(lineno)
    
    def _markdown_support(self, caller=None):
        body = Markup(caller()).unescape()
        result = do_markdown(body)
        return result