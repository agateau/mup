import codecs
import gzip
import os
import re

from pkg_resources import resource_string


_ENC_BOMS = (
    ('utf-8-sig', (codecs.BOM_UTF8,)),
    ('utf-16', (codecs.BOM_UTF16_LE, codecs.BOM_UTF16_BE)),
    ('utf-32', (codecs.BOM_UTF32_LE, codecs.BOM_UTF32_BE))
)


_template = None


def applyTemplate(html):
    global _template
    if _template is None:
        _template = resource_string("mup", "data/template.html")
    return _template.replace("%content%", html)


def _detectEncoding(head, default):
    for encoding, boms in _ENC_BOMS:
        if any(head.startswith(bom) for bom in boms):
            return encoding
    return default


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


def _readFile(fl):
    """
    Read a file as unicode, correctly handling BOM
    """
    try:
        raw = fl.read()
        encoding = _detectEncoding(raw, 'utf-8')
        return unicode(raw, encoding)
    finally:
        fl.close()


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
        src = _readFile(fl)

        src = _skipHeader(src)
        return self._doConvert(src)

    def _doConvert(self, txt):
        raise NotImplementedError
