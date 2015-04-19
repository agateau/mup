import codecs
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


def selectBestConverter(lst):
    """Select the best converter from lst. An offline converter is preferred to
    an online one. The reference implementation is preferred if it is
    available."""

    def keyForConverter(converter):
        weight = 1
        if converter.online:
            weight += 1
        if converter.reference:
            weight -= 1
        return '{}{}'.format(weight, converter.name.lower())

    lst = sorted(lst, key=keyForConverter)
    return lst[0]


def _detectEncoding(head, default):
    for encoding, boms in _ENC_BOMS:
        if any(head.startswith(bom) for bom in boms):
            return encoding
    return default


def readFile(fl):
    """
    Read a file as unicode, correctly handling BOM
    """
    try:
        raw = fl.read()
        encoding = _detectEncoding(raw, 'utf-8')
        return unicode(raw, encoding)
    finally:
        fl.close()


def skipHeader(txt):
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
