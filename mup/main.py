#!/usr/bin/env python
import argparse
import logging
import signal
import sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from window import Window


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', dest='verbose',
                        action='store_true', help='Enable debug output')
    parser.add_argument('markup_file', nargs='?')
    args = parser.parse_args()

    loglevel = logging.DEBUG if args.verbose else logging.WARNING
    logging.basicConfig(format='%(levelname)s: %(message)s',
                        level=loglevel)

    return showMainWindow(args.markup_file)


def showMainWindow(path):
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QApplication(sys.argv)

    window = Window()
    if path:
        window.load(path)

    window.show()
    return app.exec_()


if __name__ == "__main__":
    sys.exit(main())
# vi: ts=4 sw=4 et
