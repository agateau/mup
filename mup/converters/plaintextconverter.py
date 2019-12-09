import html
import os

from .converter import Converter
from .utils import applyTemplate


class PlainTextConverter(Converter):
    """
    A dumb converter which just wraps content in a <pre> tag
    """
    name = "Plain text"
    format = "txt"

    def _doConvert(self, src):
        htmlText = "<pre>{}</pre>".format(html.escape(src))
        return applyTemplate(htmlText)

    def supports(self, filename):
        _, ext = os.path.splitext(filename)
        return ext.lower() in (".txt", ".text")
