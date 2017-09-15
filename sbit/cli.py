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

""" This module contains the class and the methods used to crate parsers dedicated to the
different words of command supported by sbit.

The module will do actual processing and run the associated worker method
(one of the run_foo methods)
"""

import argparse
import textwrap
import logging
from model import Key
from model import Configuration
import run_testsuite
import check_testsuite
import check_library

# -----------------------------------------------------------------------------
#
#  Class Cli
#
# -----------------------------------------------------------------------------
class Cli(object):
  """This class represent the command line parser for this tool. It brings
  methods used to parse command line arguments then run the program itself
  """

  # -------------------------------------------------------------------------
  #
  # __init__
  #
  # -------------------------------------------------------------------------
  def __init__(self):
    """Default constructor
    """

    # Current version
    self.version = "0.2.1"

    # Create the internal parser from argparse
    self.parser = argparse.ArgumentParser(description=textwrap.dedent('''\
SBIT - Simple Build In Test v''' + self.version + '''

Available commands are :
  . ''' + Key.CHECK_LIBRARY.value + '''       Check the test scrpit library consistency
  . ''' + Key.CHECK_SUITE.value +  '''         Check the test scrpit library consistency
  . ''' + Key.RUN_SUITE.value + '''           Execute the tests defined in the given suite file
'''), formatter_class=argparse.RawTextHelpFormatter)

    # Stores the arguments from the parser
    self.args = None

    # Stores the argument in the instance
    self.command = None

    # Stores the configuration definition object (will cntains all the information
    #retrieved from the command line
    self.cfg = None



  # -------------------------------------------------------------------------
  #
  # parse
  #
  # -------------------------------------------------------------------------
  def parse(self, args):
    """ This method build the parser, add all options and run it. The result of
    parser execution is stored in a member variable.
    """

    # Stores the argument in the instance
    self.command = args

    self.__add_parser_common()

    # According to the command, call the method dedicated to parse the arguments
    if   self.command == "check-suite":
      self.__add_parser_check_suite()
    elif self.command == "check-library":
      self.__add_parser_check_library()
    elif self.command == "run-suite":
      self.__add_parser_run_suite()
    else:
      # If the command word is unknown, the force the parsing of the help flag
      logging.critical("Unknown command : %s", self.command)
      return self.parser.parse_args(['-h'])

    # Finally call the parser that has been initialized by the previous lines
    self.args = self.parser.parse_args()



  # -------------------------------------------------------------------------
  #
  # run
  #
  # -------------------------------------------------------------------------
  def run(self):
    """ According to the command, call the method dedicated to run the
      command called from cli
    """

    # Create the project definition object, and load its configuration
    self.cfg = Configuration()
    self.cfg.load_configuration()

    # ---------------------------------------------------------------------
    # Override configuration with values passed on the commande line
    # ---------------------------------------------------------------------

    # Get the log_level from command line
    if self.args.log_level != None:
      self.cfg.log_level = self.args.log_level.upper()
    # If not command line value, defaults to log
    else:
      self.cfg.log_level = Key.LOG_LEVEL_INFO.value

    # Retrieve the suite path from command line
    if self.args.suite_path != None:
      self.cfg.suite_path = self.args.suite_path

    # Retrieve the library path from command line
    if self.args.library_path != None:
      self.cfg.library_path = self.args.library_path

    # Retrieve the array of categories
    if self.args.category != None:
      self.cfg.category = self.args.category

    # Retrieve the aggregation level
    if self.args.aggregation_level != None:
      self.cfg.aggregation_level = self.args.aggregation_level

    # Set the results cache flag
    if self.args.no_result_cache != None:
      self.cfg.use_results_cache = not self.args.no_result_cache

    # Retrieve the failfast flag
    self.cfg.fail_fast = bool(self.args.fail_fast != None)

    # Retrieve the show hints flag
    self.cfg.show_hints = bool(self.args.show_hints != None)

    # Create the logger object
    logging.basicConfig()
    self.cfg.logging = logging.getLogger()
    self.cfg.logging.setLevel(self.cfg.log_level)

    # Select the method to run according to the command
    if self.command == Key.CHECK_LIBRARY.value:
      self.__run_check_library()
    elif self.command == Key.CHECK_SUITE.value:
      self.__run_check_suite()
    elif self.command == Key.RUN_SUITE.value:
      self.__run_run_suite()
    else:
      self.cfg.logging.critical("Unnown command : %s", self.command)
      exit(1)


  # -------------------------------------------------------------------------
  #
  # __add_parser_common
  #
  # -------------------------------------------------------------------------
  def __add_parser_common(self):
    """ This method add parser options common to all command
    Configuration file store the definition of rootfs. Option can be
    overriden by arguments on the command line (like --log-level)
    """

    # Defines the level of the log to output
    self.parser.add_argument(Key.OPT_LOG_LEVEL.value,
                             action='store',
                             dest=Key.LOG_LEVEL.value,
                             choices=['debug', 'info', 'warning', 'error', 'critical'],
                             help="defines the minimal log level. Default value is  warning")

    self.parser.add_argument(Key.OPT_LIBRARY_PATH.value,
                             action='store',
                             dest=Key.LIBRARY_PATH.value,
                             help="path to the directory storing the test scripts")

    self.parser.add_argument(Key.OPT_SUITE_PATH.value,
                             action='store',
                             dest=Key.SUITE_PATH.value,
                             help="path to the file containing the test suite (YAML format)")

    self.parser.add_argument(Key.OPT_FAIL_FAST.value,
                             action='store_true',
                             dest=Key.FAIL_FAST.value,
                             help="if this flag is activated, sbit will stop at the first error"
                                  "encountered, otherwise it will continue to run as long as"
                                  " possible and will report all errors")

    self.parser.add_argument(Key.OPT_SHOW_HINTS.value,
                             action='store_true',
                             dest=Key.SHOW_HINTS.value,
                             help="if this flag is activated, sbit will display hints when the "
                                  "tests fails. Hints have to be defined in the tests scripts and"
                                  " are optionals")


  # -------------------------------------------------------------------------
  #
  # __add_parser_check_suite
  #
  # -------------------------------------------------------------------------
  def __add_parser_check_suite(self):

    """ This method add parser options specific to check validity and syntax
    of the test suite.
    """

    self.parser.add_argument(Key.CHECK_SUITE.value,
                             help=Key.OPT_HELP_COMMAND.value)



  # -------------------------------------------------------------------------
  #
  # __add_parser_check_library
  #
  # -------------------------------------------------------------------------
  def __add_parser_check_library(self):

    """ This method add parser options specific to check validity of the test
    script library content (meta data, unique ids, etc.)
    """

    self.parser.add_argument(Key.CHECK_LIBRARY.value,
                             help=Key.OPT_HELP_COMMAND.value)



  # -------------------------------------------------------------------------
  #
  # __add_parser_run_suite
  #
  # -------------------------------------------------------------------------
  def __add_parser_run_suite(self):

    """ This method add parser options specific to the test suite execution
    smethod.
    """

    self.parser.add_argument(Key.RUN_SUITE.value,
                             help=Key.OPT_HELP_COMMAND.value)

    # Defines the reverse order search path
    self.parser.add_argument(Key.OPT_CATEGORY.value,
                             action='store',
                             nargs='*',
                             dest=Key.CATEGORY.value,
                             help="Defines the list of test category to execute")

    # Defines the reverse order search path
    self.parser.add_argument(Key.OPT_AGGREGATION_LEVEL.value,
                             action='store',
                             dest=Key.AGGREGATION_LEVEL.value,
                             help="defines the test depth used for results aggreation")

    # Defines the reverse order search path
    self.parser.add_argument(Key.OPT_NO_RESULT_CACHE.value,
                             action='store_true',
                             dest=Key.NO_RESULT_CACHE.value,
                             help="deactivate script result cache (scripts can be run n times)")

  # -------------------------------------------------------------------------
  #
  # __run_check_library
  #
  # -------------------------------------------------------------------------
  def __run_check_library(self):
    """ Method used to handle the check_library command.
      Create the business objet, then execute the entry point
    """

    # Create the business object
    command = check_library.CheckLibrary(self.cfg)

    # Then call the dedicated method
    command.check_library()



  # -------------------------------------------------------------------------
  #
  # __run_check_suite
  #
  # -------------------------------------------------------------------------
  def __run_check_suite(self):
    """ Method used to handle the check_library command.
      Create the business objet, then execute the entry point
    """

    # Create the business object
    command = check_testsuite.CheckTestSuite(self.cfg)

    # Then call the dedicated method
    command.check_suite()



  # -------------------------------------------------------------------------
  #
  # __run_run_suite
  #
  # -------------------------------------------------------------------------
  def __run_run_suite(self):
    """ Method used to handle the check_library command.
      Create the business objet, then execute the entry point
    """

    # Create the business object
    command = run_testsuite.RunTestSuite(self.cfg)

    # Then call the dedicated method
    command.run_suite()
