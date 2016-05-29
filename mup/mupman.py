#!/usr/bin/env python3
import argparse
import subprocess
import sys

from mup.main import showMainWindow


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--nofork', dest='foreground',
                        action='store_true', help='Foreground: Do not fork at startup')
    parser.add_argument('section', nargs='?')
    parser.add_argument('page')

    args = parser.parse_args()

    cmd = ['man', '--where']
    if args.section:
        cmd.append(args.section)
    cmd.append(args.page)
    try:
        path = subprocess.check_output(cmd).strip().decode('utf-8')
    except subprocess.CalledProcessError as exc:
        return 1

    return showMainWindow(path, foreground=args.foreground)


if __name__ == '__main__':
    sys.exit(main())
# vi: ts=4 sw=4 et
