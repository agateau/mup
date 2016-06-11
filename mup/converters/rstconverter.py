import os

import docutils.core

from .converter import Converter


class RstConverter(Converter):
    name = "RST"
    reference = True

    def _doConvert(self, txt):
        out = docutils.core.publish_string(txt, writer_name="html")
        return out.decode("utf-8")

    def supports(self, filename):
        _, ext = os.path.splitext(filename)
        return ext.lower() == ".rst"
