import os

from .converter import Converter


class HtmlConverter(Converter):
    """
    A dumb converter which just passes content unaltered
    """
    name = "Straight HTML"

    def _doConvert(self, src):
        return src

    def supports(self, filename):
        _, ext = os.path.splitext(filename)
        return ext.lower() in (".htm", ".html")
