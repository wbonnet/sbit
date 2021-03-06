#
# The contents of this file are subject to the Apache 2.0 license you may not
# use this file except in compliance with the License.
#
# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
# for the specific language governing rights and limitations under the
# License.
#
#
# Copyright 2017 SBIT project (http://www.firmwaretoolkit.org).
# All rights reserved. Use is subject to license terms.
#
#
# Contributors list :
#
#    William Bonnet     wllmbnnt@gmail.com, wbonnet@theitmakers.com
#

from sbit.release import __version__, __author__, __author_email__

try:
    from setuptools import setup

except ImportError:
    from distutils.core import setup

config = {
    'description': 'Simple Buid In Tests',
    'long_description': 'SBIT is a tool designed to run Simple Build In Tests. Tests are defined in a YAML file describing a hierchical structure of tests. Tests themselves are bash scripts stored in a test library',
    'author': __author__,
    'url': 'https://github.com/wbonnet/sbit/',
    'download_url': 'https://github.com/wbonnet/sbit/',
    'author_email': __author_email__,
    'version': __version__,
    'install_requires': [ 'pyyaml' ],
    'packages': ['sbit'],
    'scripts': [ 'bin/sbit' ],
    'name': 'sbit'
}

setup(**config)
