#!/usr/bin/env python
import argparse
import logging
import os
import signal
import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from window import Window


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', dest='verbose',
                        action='store_true', help='Enable debug output. Implies --nofork')
    parser.add_argument('-f', '--nofork', dest='foreground',
                        action='store_true', help='Foreground: Do not fork at startup')
    parser.add_argument('markup_file', nargs='?')
    args = parser.parse_args()

    loglevel = logging.DEBUG if args.verbose else logging.WARNING
    logging.basicConfig(format='%(levelname)s: %(message)s',
                        level=loglevel)

    if args.verbose:
        args.foreground = True

    return showMainWindow(args.markup_file, foreground=args.foreground)


def showMainWindow(path, foreground=False):
    if not foreground:
        # Close stdout and stderr to avoid polluting the terminal
        os.close(1)
        os.close(2)

        if os.fork() > 0:
            return

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
