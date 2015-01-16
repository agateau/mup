#!/usr/bin/env python
# encoding: utf-8

# Python 2/3 compatibility
from __future__ import division, absolute_import, print_function, unicode_literals

import argparse
import json
import requests
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', default='markdown')
    args = parser.parse_args()

    payload = {
        'mode': args.mode,
        'text': sys.stdin.read()
    }
    headers = {
        'content-type': 'application/json'
    }
    rs = requests.post('https://api.github.com/markdown',
            data=json.dumps(payload), headers=headers)

    if rs.status_code == 200:
        print(rs.text)
        return 0
    else:
        print(rs.text, file=sys.stderr)
        return rs.status_code


if __name__ == '__main__':
    sys.exit(main())
# vi: ts=4 sw=4 et