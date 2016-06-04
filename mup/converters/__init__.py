import os
import logging

from xdg import BaseDirectory

from .htmlconverter import HtmlConverter
from .processconverter import ProcessConverter


_converters = []


def _loadConvertersFromDir(configDir):
    for name in os.listdir(configDir):
        _, ext = os.path.splitext(name)
        if ext != ".yaml":
            continue
        fullPath = os.path.join(configDir, name)
        converter = ProcessConverter.fromConfigFile(fullPath)
        if converter is None:
            continue
        if converter.isAvailable():
            yield converter
        else:
            logging.info('{} is not available'.format(converter.name))


def init():
    global _converters

    for convertersDir in BaseDirectory.load_data_paths("mup/converters"):
        _converters.extend(_loadConvertersFromDir(convertersDir))

    try:
        from .markdownconverter import MarkdownConverter
        _converters.append(MarkdownConverter())
    except ImportError:
        logging.info('Failed to load internal Markdown converter, skipping.')

    try:
        from .rstconverter import RstConverter
        _converters.append(RstConverter())
    except ImportError:
        logging.info('Failed to load internal rST converter, skipping.')

    _converters.append(HtmlConverter())

    _converters.sort(key=lambda x: x.name)
    return _converters


def findConverters(filepath):
    filename = os.path.basename(filepath)
    remaining, ext = os.path.splitext(filename)
    if ext == '.gz':
        filename = remaining
    return [x for x in _converters if x.supports(filename)]
