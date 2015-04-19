from StringIO import StringIO
from unittest import TestCase

from mup.converters import converter
from mup.converters.converter import Converter
from mup.converters.utils import selectBestConverter

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

    def testSelectBestConverter(self):
        def mkconverter(online=False, reference=False):
            converter = Converter()
            converter.online = online
            converter.reference = reference
            return converter

        online = mkconverter(online=True)
        reference = mkconverter(reference=True)
        normal = mkconverter()

        self.assertEquals(selectBestConverter([online, reference, normal]), reference)
        self.assertEquals(selectBestConverter([online, normal]), normal)
