#!/usr/bin/env python
# encoding: utf-8
"""
MUP: Markup previewer

:copyright: 2012-2014 Aurélien Gâteau.
:license: BSD.
"""
import os

from setuptools import setup

import mup

DESCRIPTION = "Markup previewer"

CONVERTERS_DIR = 'share/mup/converters'
CONVERTERS = [os.path.join(CONVERTERS_DIR, x) for x in os.listdir(CONVERTERS_DIR) if x.endswith(".yaml")]

setup(name=mup.__appname__,
    version=mup.__version__,
    description=DESCRIPTION,
    author="Aurélien Gâteau",
    author_email="mail@agateau.com",
    license=mup.__license__,
    platforms=["any"],
    url="http://github.com/agateau/mup",
    install_requires=["pyxdg"],
    packages=["mup", "mup.converters"],
    package_data={
        "mup": ["data/*.html"],
    },
    data_files=[
        ('share/applications', ['share/applications/mup.desktop']),
        ('share/mup/converters', CONVERTERS),
    ],
    entry_points={
        "console_scripts": [
            "mup-gh-markdown = mup.converters.ghmarkdown:main",
        ],
        "gui_scripts": [
            "mup = mup.main:main",
            "mupman = mup.mupman:main",
        ]
    }
)
