#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os
from setuptools import find_packages, setup


# Package meta-data.
NAME = 'texttv'
DESCRIPTION = 'SVT Text-TV browser in the terminal.'
URL = 'https://github.com/Crablicious/texttv'
EMAIL = 'adwe@live.se'
AUTHOR = 'Adam Wendelin'
REQUIRES_PYTHON = '>=3.5.0'
VERSION = None

# What packages are required for this module to be executed?
REQUIRED = [
]

EXTRAS = {
}

# The rest you shouldn't have to touch too much :)
# ------------------------------------------------
# Except, perhaps the License and Trove Classifiers!
# If you do change the License, remember to change the Trove Classifier for that!

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Load the package's __version__.py module as a dictionary.
about = {}
if not VERSION:
    with open(os.path.join(here, NAME, '__version__.py')) as f:
        exec(f.read(), about)
else:
    about['__version__'] = VERSION


# Where the magic happens:
setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=('tests',)),
    # package_dir = {'': 'texttv'},
    # py_modules=['texttv.page_handler', 'texttv.utils', 'texttv.tbls'],
    entry_points={
        'console_scripts': ['texttv=texttv.__main__:main'],
    },
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    include_package_data=True,
    license='GPLv3',
    classifiers=[
        # https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],
    cmdclass={
    },
)
