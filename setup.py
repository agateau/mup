#!/usr/bin/env python
# encoding: utf-8
"""
MUP: Markup previewer

:copyright: 2012-2014 Aurélien Gâteau.
:license: BSD.
"""

from setuptools import setup

import mup

DESCRIPTION = "Markup previewer"

setup(name=mup.__appname__,
    version=mup.__version__,
    description=DESCRIPTION,
    author="Aurélien Gâteau",
    author_email="mail@agateau.com",
    license=mup.__license__,
    platforms=["any"],
    url="http://github.com/agateau/mup",
    packages=["mup", "mup.converters"],
    package_data={
        "mup": ["data/*.html", "config/*.conf"],
    },
    data_files=[
        ('share/applications', ['desktop/mup.desktop'])
    ],
    entry_points={
        "gui_scripts": [
            "mup = mup.mup:main",
        ]
    }
)
