import fnmatch

import markdown

from .converter import Converter
from .utils import applyTemplate


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
