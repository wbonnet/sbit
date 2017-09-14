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
# Copyright 2017 DFT project (http://www.debianfirmwaretoolkit.org).
# All rights reserved. Use is subject to license terms.
#
#
# Contributors list :
#
#    William Bonnet     wllmbnnt@gmail.com, wbonnet@theitmakers.com
#
#


""" This modules implements the functionnalities used to check consistency of a test library.
Consistency checks will control library content and search for redundant IDs, scripts with execution
flag, invalid meta data, etc.
"""

import logging
from cli_command import CliCommand

#
#    Class CheckLibrary
#
class CheckLibrary(CliCommand):
  """This class implements methods needed to load a test library from the configuration files,
  and control its validity (meta data and unique ids).

  Results are display to output according to parameters from the command line. These paraeters
  are stored in the configuration object by the CLI parser.
  """

  # -------------------------------------------------------------------------
  #
  # __init__
  #
  # -------------------------------------------------------------------------
  def __init__(self, cfg):
    """Default constructor
    """

    # Initialize ancestor
    CliCommand.__init__(self, cfg)



  # -------------------------------------------------------------------------
  #
  # check_library
  #
  # -------------------------------------------------------------------------
  def check_library(self):
    """This method implement the business logic of check a test library.
    Checking a test suite is :
    . Check tests meta data
    . Test syntax
    . Uniques IDs for each test
    """

    # Check that there is a firmware configuration file first
    if self.cfg is None:
      logging.critical("The configuration file object is not defined")
      exit(1)

    print("check_library")

    if self.cfg.library_path:
      print(self.cfg.library_path)

    if self.cfg.suite_path:
      print(self.cfg.suite_path)
