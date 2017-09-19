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
# Copyright 2016 William Bonnet.
# All rights reserved. Use is subject to license terms.
#
#
# Contributors list :
#
#    William Bonnet 	wbonnet@theitmakers.com
#
#

try:
    from setuptools import setup

except ImportError:
    from distutils.core import setup

config = {
    'description': 'Simple Buid In Tests',
    'long_description': 'SBIT is a tool designed to run Simple Build In Tests. Tests are defined in a YAML file describing a hierchical structure of tests. Tests themselves are bash scripts stored in a test library',
    'author': 'William Bonnet',
    'url': 'https://github.com/wbonnet/sbit/',
    'download_url': 'https://github.com/wbonnet/sbit/',
    'author_email': 'wbonnet@theitmakers.com',
    'version': '0.2.2',
    'install_requires': [ 'pyyaml' ],
    'packages': ['sbit'],
    'scripts': [ 'bin/sbit' ],
    'name': 'sbit'
}

setup(**config)
