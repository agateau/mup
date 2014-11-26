import gzip
import os
import re


def loadDataFile(filename):
    dataDir = os.path.dirname(__file__)
    filepath = os.path.join(dataDir, filename)
    return unicode(open(filepath).read(), "utf-8")


_template = None


def applyTemplate(html):
    global _template
    if _template is None:
        _template = loadDataFile("template.html")
    return _template.replace("%content%", html)


def _skipHeader(txt):
    """
    Skip any yaml header, if present
    """
    rx = re.compile("^[-a-zA-Z0-9_]+:")
    if not rx.match(txt):
        return txt

    src = txt.split("\n")
    for pos, line in enumerate(src):
        if line == "":
            # We passed the header
            return "\n".join(src[pos+1:])
    return ""


class Converter(object):
    name = 'Unnamed'

    def supports(self, filepath):
        raise NotImplementedError

    def convert(self, filename):
        ext = os.path.splitext(filename)[1]
        if ext == '.gz':
            fl = gzip.open(filename)
        else:
            fl = open(filename)
        try:
            src = unicode(fl.read(), "utf-8")
        finally:
            fl.close()

        src = _skipHeader(src)
        return self._doConvert(src)

    def _doConvert(self, txt):
        raise NotImplementedError
