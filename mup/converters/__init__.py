import os


from htmlconverter import HtmlConverter
from processconverter import ProcessConverter


_converters = []


def init(converterConfigList):
    global _converters

    for dct in converterConfigList:
        converter = ProcessConverter(dct["name"], cmd=dct["cmd"],
                                     args=dct.get("args"),
                                     matches=dct["matches"])
        if converter.isAvailable():
            _converters.append(converter)

    try:
        from markdownconverter import MarkdownConverter
        _converters.append(MarkdownConverter())
    except ImportError:
        print('Failed to load internal Markdown converter, skipping.')
        pass

    try:
        from rstconverter import RstConverter
        _converters.append(RstConverter())
    except ImportError:
        print('Failed to load internal rST converter, skipping.')
        pass

    _converters.append(HtmlConverter())
    return _converters


def findConverters(filepath):
    filename = os.path.basename(filepath)
    remaining, ext = os.path.splitext(filename)
    if ext == '.gz':
        filename = remaining
    return [x for x in _converters if x.supports(filename)]
