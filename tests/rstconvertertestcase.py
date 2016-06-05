from unittest import TestCase

from mup.converters.rstconverter import RstConverter


class RstConverterTestCase(TestCase):
    def test_doConvert(self):
        converter = RstConverter()

        output = converter._doConvert("hello")
        self.assertTrue(isinstance(output, str))
        self.assertTrue("hello" in output)
