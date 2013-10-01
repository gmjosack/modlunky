#!/usr/bin/env python

from distutils.core import setup

execfile('modlunky/version.py')

with open('requirements.txt') as requirements:
    required = requirements.read().splitlines()

kwargs = {
    "name": "modlunky",
    "version": str(__version__),
    "packages": ["modlunky"],
    "scripts": ["bin/modlunky"],
    "description": "Library and Command Line Tool for Spelunky.",
    "author": "Gary M. Josack",
    "maintainer": "Gary M. Josack",
    "author_email": "gary@byoteki.com",
    "maintainer_email": "gary@byoteki.com",
    "license": "MIT",
    "url": "https://github.com/gmjosack/modlunky",
    "download_url": "https://github.com/gmjosack/modlunky/archive/master.tar.gz",
    "classifiers": [
        "Programming Language :: Python",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ]
}

if required:
    kwargs["install_requires"] = required

setup(**kwargs)

