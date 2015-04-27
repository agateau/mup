import gzip
import os

from mup.converters.utils import readFile, skipHeader


class Converter(object):
    name = 'Unnamed'
    # Set to True if this converter wraps the reference implementation for the
    # markup it supports
    reference = False
    # Set to True if this converter uses online tools
    online = False

    def supports(self, filepath):
        raise NotImplementedError

    def convert(self, filename):
        ext = os.path.splitext(filename)[1]
        if ext == '.gz':
            fl = gzip.open(filename)
        else:
            fl = open(filename)
        src = readFile(fl)

        src = skipHeader(src)
        return self._doConvert(src)

    def _doConvert(self, txt):
        raise NotImplementedError
