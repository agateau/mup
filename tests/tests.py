#!/usr/bin/env python3
import os
import unittest
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), os.pardir))

from converterstestcase import *
from rstconvertertestcase import *

def main():
    unittest.main()

if __name__ == "__main__":
    main()
# vi: ts=4 sw=4 et
