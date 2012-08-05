import fnmatch
import os

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


class MarkdownConverter(object):
    MATCHES = ["*.md", "*.mkd", "*.markdown"]

    def __init__(self):
        dataDir = os.path.dirname(__file__)
        templateFilename = os.path.join(dataDir, "template.html")
        self.template = unicode(open(templateFilename).read(), "utf-8")

    def convert(self, txt):
        return self.template.replace("%content%", markdown.markdown(txt))


class RstConverter(object):
    MATCHES = ["*.rst"]

    def convert(self, txt):
        return docutils.core.publish_string(txt, writer_name="html")


class HtmlConverter(object):
    """
    A dumb converter which just passes content unaltered
    """
    MATCHES = ["*.html", "*.htm"]

    def convert(self, src):
        return src

def _init():
    lst = []

    if HAS_MARKDOWN:
        lst.append(MarkdownConverter())

    if HAS_DOCUTILS:
        lst.append(RstConverter())

    lst.append(HtmlConverter())
    return lst

_converters = _init()


def _findConverter(filename):
    for converter in _converters:
        for match in converter.MATCHES:
            if fnmatch.fnmatch(filename, match):
                return converter
    return None

def canHandle(filename):
    return _findConverter(filename) is not None

def convert(filename):
    converter = _findConverter(filename)
    if not converter:
        print "Don't know how to convert file '%s'. Maybe you need to install a module for it?" % filename
        return
    src = unicode(open(filename).read(), "utf-8")
    return converter.convert(src)
