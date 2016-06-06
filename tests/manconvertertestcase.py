import os
import re

from unittest import TestCase

import yaml

from mup.converters import man

TEST_DIR = os.path.dirname(__file__)


MAN_PAGE_DICT = {
    ('foo', '1'): '/man/1/foo.1',
    ('bar', '3'): '/man/3/bar.3',
}


def fake_find_man_page(name, section):
    try:
        return MAN_PAGE_DICT[(name, section)]
    except KeyError:
        return None


def run_test(test_case, data_dir):
    input_dir = os.path.join(data_dir, 'input')
    test_names = os.listdir(input_dir)
    for test_name in test_names:
        if test_name[0] == '.':
            continue
        input_path = os.path.join(input_dir, test_name)
        with open(input_path, 'rt') as fp:
            out = man.convert(fp, find_man_page_fcn=fake_find_man_page)

        expected_path = os.path.join(data_dir, 'expected', test_name + '.yaml')
        with open(expected_path, 'rt') as fp:
            dct = yaml.load(fp)
        patterns = dct['patterns']

        for pattern in patterns:
            with test_case.subTest(test_name=test_name, pattern=pattern):
                if not re.search(pattern, out, re.MULTILINE):
                    test_case.fail(out)


class ManConverterTestCase(TestCase):
    def test(self):
        data_dir = os.path.join(TEST_DIR, 'manconverterdata')
        run_test(self, data_dir)
