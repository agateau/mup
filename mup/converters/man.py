#!/usr/bin/env python
# encoding: utf-8

# Python 2/3 compatibility
from __future__ import division, absolute_import, print_function, unicode_literals

import argparse
import subprocess
import sys


CMD = ['groff', '-K', 'utf-8', '-mandoc', '-Thtml']


def main():
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    popen = subprocess.Popen(CMD, stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = popen.communicate(sys.stdin.read())

    # Turn '&minus' back into '-' so that options (-f, --quiet...) are easier to
    # search
    stdout = stdout.replace('&minus;', '-')
    print(stdout)
    return 0


if __name__ == '__main__':
    sys.exit(main())
# vi: ts=4 sw=4 et
