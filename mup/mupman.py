#!/usr/bin/env python
import argparse
import subprocess
import sys

from main import showMainWindow


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('section', nargs='?')
    parser.add_argument('page')

    args = parser.parse_args()

    cmd = ['man', '--where']
    if args.section:
        cmd.append(args.section)
    cmd.append(args.page)
    try:
        path = subprocess.check_output(cmd).strip()
    except subprocess.CalledProcessError as exc:
        return 1

    return showMainWindow(path)


if __name__ == '__main__':
    sys.exit(main())
# vi: ts=4 sw=4 et
