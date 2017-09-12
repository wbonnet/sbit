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


""" This modules implements the functionnalities used to create (from the yaml structure)
and run a test suite, either from top level category or from any midlevel or subcategory.
"""

import logging
import os
import stat
import tempfile
import datetime
import random
import time
from cli_command import CliCommand
from model import Key
from model import TestSuite
from ansi_colors import Colors

# -----------------------------------------------------------------------------
#
#    Class RunTestuite
#
# -----------------------------------------------------------------------------
class RunTestSuite(CliCommand):
  """This class implements methods needed to load a test suite from the
  configuration files, run it, and sumarize tests resuts.

  Results are display to output according to parameters from the command line.
  These paraeters are stored inthe configurationobject by the CLI parser
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
  # run_suite
  #
  # -------------------------------------------------------------------------
  def run_suite(self):
    """This method implement the business logic of running a test suite.
    Runing test suite is made of several steps ientified below.

    It calls dedicated method for each step. The main steps are :
    .
    """

    # Check that there is a configuration file first
    if self.cfg is None:
      logging.critical("The configuration file object is not defined")
      exit(1)

    # Instanciate a TestSuite object and load its content from the YAML file
    self.suite = TestSuite()
    self.suite.load(self.cfg.suite_path)

    # Check that the path to script library is defined (can come from config file or command line)
    if self.cfg.library_path:
      logging.debug("Using library path : " + self.cfg.library_path)
    else:
      logging.critical("The library path is not defined")
      exit(1)

    # Check that the path to test suite file is defined (can come from config file or command line)
    if self.cfg.suite_path:
      logging.debug("Using test suite : " + self.cfg.suite_path)
    else:
      logging.critical("The suite path is not defined")
      exit(1)

    # Check that the path to test suite file is defined (can come from config file or command line)
    if self.cfg.category is None or len(self.cfg.category) == 0:
      # No category given, then add all the root categories
      self.cfg.category = []
      for suite in self.suite.suite:
        self.cfg.category.append(suite[Key.CATEGORY.value])

    # Iterate the list of categories and call the run test category method
    for category in self.cfg.category:
      self.find_category_and_run_test(category)


  # -------------------------------------------------------------------------
  #
  # find_category_and_run_test
  #
  # -------------------------------------------------------------------------
  def find_category_and_run_test(self, category):
    """This method search for the given category, then execute recursively
    all the tst defined at its level, then at the sub level. Category can be
     either the root of the tree, or a sub category.

    The root will be defined as "category", an subcategories as :
      "category:subcategory1:subsubcategory2"
    """

    #
    # Seek the given category in the test tree
    #

    # First let's split the category in its component names (aka tokens)
    tokens = category.split(":")

    # And now let's walk in the tree
    categories = self.suite.suite

    # counter used to know how many toeksn have been processed so far
    counter = 0

    # Iterate the full tokens array
    while counter < len(tokens):

      # Use a flag to know if the search tokens has been found or not
      token_was_found = False

      # Iterate the categories at this level
      for cur in categories:
        # And test if we have fond the searched category
        if cur[Key.CATEGORY.value].lower() == tokens[counter].lower():
          # Mark token as found
          token_was_found = True

          # Update current category
          if Key.TEST_SUITE.value in cur:
            categories = cur[Key.TEST_SUITE.value]
          else:
            categories = {}
            categories[0] = cur

          # Have we reached the end of the tokens list ?
          if counter == len(tokens) - 1:
            # Yes, thus exit this loop
            categories = {}
            categories[0] = cur
            break;
          else:
            # Not yet, let's goo deeper
            continue

      # Check if we have found something or not ?
      if not token_was_found:
        self.cfg.logging.critical("The token " + tokens[counter] + " defined in the category to "
                                  "execute was not found in the test suite definition file")
        exit(1)

      # Increment the tokens counter
      counter += 1

    # Category has been found. Now let's recurse...
    print ("[+] " + Colors.FG_YELLOW.value + Colors.BOLD.value + categories[0][Key.CATEGORY.value] \
           + Colors.RESET.value)
    print ("------------------------------------")
    print (" " + categories[0][Key.SHORT_DESCRIPTION.value])
    msg_buffer = []
    self.execute_category_test_and_recurse(categories[0], output_msg=msg_buffer)
    print ("")



  # -------------------------------------------------------------------------
  #
  # execute_category_test_and_recurse
  #
  # -------------------------------------------------------------------------
  def execute_category_test_and_recurse(self, category, current_level = 0, output_msg = None):
    """This method is in charge of doing real test execution, and recurse down
    to the test tree (going down in the subcategories).
    """

    # Generate a local output buffer
    local_msg = []

    # Generate output string
    output = ""
    output = "".join("  " for i in range(current_level))
    output += " - Testing " + category[Key.CATEGORY.value]

    # Flags used to mark if the locally defined and subcategories tests were successfull
    success_local = True
    success_subtest = True

    # Execute test defined at category level
    print(category)
    if not Key.TEST.value in category:
      logging.debug("No test defined in category " + category[Key.CATEGORY.value])
    else:
      for test in category[Key.TEST.value]:
        # Generate the output message
        test_output = "".join("  " for i in range(current_level))
        test_output += "   - Running : " + test[Key.SCRIPT.value]
        test_output += "".join(" " for i in range(64 - len(test_output)))

        # Generate the path to the real test
        script_path = self.cfg.library_path + "/" + test[Key.SCRIPT.value]

        # Check that the script exist and is executable
        ret = -1
        if not os.path.isfile(script_path) or not os.access(script_path, os.X_OK):
          logging.error("Script " + script_path +" does not exist. Mark test as failed.")
          ret = -1
        # Script exist, we can try to execute it
        else:
          # If args are defined, concatenate to the script command line
          if Key.ARGS.value in test:
            script_path += " " + test[Key.ARGS.value]

          # Finaly execute the test script
          ret, out, err = self.execute_command(script_path)

        # And generate a random result
        if ret == 0:
          success_local &= True
          test_output += "[" + Colors.FG_GREEN.value + Colors.BOLD.value + " OK "
          test_output += Colors.RESET.value + "]"
        else:
          success_local &= False
          test_output += "[" + Colors.FG_RED.value + Colors.BOLD.value + " KO "
          test_output += Colors.RESET.value + "]"

        # Push the line to output to the message buffer only if below aggregation level
        if self.cfg.aggregation_level is None or (current_level < int(self.cfg.aggregation_level)):
          local_msg.append(test_output)

    # Add string right padding to align at 64
    output += "".join(" " for i in range(64 - len(output)))

    # Iterate the sub cateries and recursivly execute tests
    if Key.TEST_SUITE.value in category:
      # For each sub category in the test suite
      for cur in category[Key.TEST_SUITE.value]:
        # Recurse suite tree
        r,o = self.execute_category_test_and_recurse(cur, current_level + 1, output_msg)

        # Then use the return values to compute the new subtest state
        success_subtest &= r

        # Concatenate the string buffers
        local_msg += o

    # Were local tests sucessful ? yes thus a green OK
    if success_local:
      if success_subtest:
        output += "[" + Colors.FG_GREEN.value + Colors.BOLD.value + " OK "
        output += Colors.RESET.value + "]"
      else:
        # We have to deal now with the case of "no local tests". If no local test are defined,
        # thus it has to go red and not orange
        if not Key.TEST.value in category:
          output += "[" + Colors.FG_RED.value + Colors.BOLD.value + " KO "
          output += Colors.RESET.value + "]"
        else:
          output += "[" + Colors.FG_ORANGE.value + Colors.BOLD.value + " Partiel "
          output += Colors.RESET.value + "]"
    else:
      # Nope... thus a red KO
      output += "[" + Colors.FG_RED.value + Colors.BOLD.value + " KO " + Colors.RESET.value + "]"

    # Push the line to output to the message buffer only if below aggregation level
    if self.cfg.aggregation_level is None or (current_level < int(self.cfg.aggregation_level)):
      local_msg.insert(0, output)

    # Concatenate local and output buffers
    output_msg = local_msg + output_msg

    # If we are back to top level, the print the message buffer
    if current_level == 0:
      for msg in output_msg:
        print(msg)

    # Return the local test result and the subtest result
    return(success_local & success_subtest, output_msg)
