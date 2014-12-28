import os

import yaml

from xdg import BaseDirectory

from htmlconverter import HtmlConverter
from processconverter import ProcessConverter


_converters = []


def _loadConvertersFromDir(configDir):
    for name in os.listdir(configDir):
        _, ext = os.path.splitext(name)
        if ext != ".conf":
            continue
        with open(os.path.join(configDir, name)) as fp:
            dct = yaml.load(fp)

        converter = ProcessConverter(dct["name"], cmd=dct["cmd"],
                                     args=dct.get("args"),
                                     matches=dct["matches"])
        if converter.isAvailable():
            yield converter


def init():
    global _converters

    for convertersDir in BaseDirectory.load_data_paths("mup/converters"):
        _converters.extend(_loadConvertersFromDir(convertersDir))

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
