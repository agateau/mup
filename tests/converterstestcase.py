from unittest import TestCase

import converters

class ConvertersTestCase(TestCase):
    def testSkipHeader(self):
        data = [
            ("key:value\n\nHello", "Hello"),
            ("key1: value1\nkey2: value2\n\nBye", "Bye"),
            ("Plain text", "Plain text"),
            ]
        for src, expected in data:
            dst = converters._skipHeader(src)
            self.assertEquals(dst, expected)
