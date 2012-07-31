#!/usr/bin/env python
import signal
import sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from window import Window

def main():
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QApplication(sys.argv)

    if len(sys.argv) != 2:
        print "USAGE: mdview <file.md>"
        return 1

    window = Window(sys.argv[1])

    window.show()
    app.exec_()
    return 0

if __name__ == "__main__":
    sys.exit(main())
# vi: ts=4 sw=4 et
