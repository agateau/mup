import fnmatch
import os
import re

try:
    import docutils.core
    HAS_DOCUTILS = True
except ImportError:
    HAS_DOCUTILS = False

try:
    import markdown
    HAS_MARKDOWN = True
except ImportError:
    HAS_MARKDOWN = False


from converter import Converter, applyTemplate
from processconverter import ProcessConverter


class MarkdownConverter(Converter):
    name = "python-markdown"

    def _doConvert(self, txt):
        html = markdown.markdown(txt)
        return applyTemplate(html)

    def supports(self, filename):
        MATCHES = ["*.md", "*.mkd", "*.markdown", "README"]
        for match in MATCHES:
            if fnmatch.fnmatch(filename, match):
                return True
        return False


class RstConverter(Converter):
    name = "RST"

    def _doConvert(self, txt):
        return docutils.core.publish_string(txt, writer_name="html")

    def supports(self, filename):
        _, ext = os.path.splitext(filename)
        return ext.lower() == ".rst"


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


def _init():
    lst = []

    lst.append(ProcessConverter("Pandoc", "pandoc", ["*.md", "*.mkd", "*.markdown", "README"]))

    if HAS_MARKDOWN:
        lst.append(MarkdownConverter())

    if HAS_DOCUTILS:
        lst.append(RstConverter())

    lst.append(HtmlConverter())
    return lst

_converters = _init()


def findConverters(filepath):
    filename = os.path.basename(filepath)
    return [x for x in _converters if x.supports(filename)]
