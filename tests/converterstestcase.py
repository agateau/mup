from StringIO import StringIO
from unittest import TestCase

from mup.converters import converter

class ConvertersTestCase(TestCase):
    def testSkipHeader(self):
        data = [
            ("key:value\n\nHello", "Hello"),
            ("key1: value1\nkey2: value2\n\nBye", "Bye"),
            ("Plain text", "Plain text"),
            ]
        for src, expected in data:
            dst = converter._skipHeader(src)
            self.assertEquals(dst, expected)

    def testReadFile(self):
        data = [
            ("\xef\xbb\xbfFoo", u"Foo"),
            ("Bar", u"Bar"),
            ]

        for src, expected in data:
            fl = StringIO(src)
            dst = converter._readFile(fl)
            self.assertEquals(dst, expected)
