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

""" This module implements The base class and functionnalities used by all the
cli targets.
"""

import subprocess
from model import Key

#
#    Class CliCommand
#
class CliCommand(object):
  """This class implements the base class used for all command from cli

     It provides method used in all the derivated command, such has
     command execution and error handling, qemu setup and tear down, etc
  """

  # -------------------------------------------------------------------------
  #
  # __init__
  #
  # -------------------------------------------------------------------------
  def __init__(self, configuration):
    """Default constructor
    """

    # Object storing the configuration definition. holds all the
    # configuration and definition used by the different stage of
    # the tool execution
    self.cfg = configuration



  # -------------------------------------------------------------------------
  #
  # execute_command
  #
  # -------------------------------------------------------------------------
  def execute_command(self, command):
    """ This method run a command as a subprocess. Typical use case is
    running commands.

    This method is a wrapper to subprocess.run , and will be moved soon
    in a helper object. It provides mutalisation of error handling
    """

    self.cfg.logging.debug("running : " + command)

    try:
      # Execute the subprocess, output ans errors are piped
      completed = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                 shell=True, check=True, universal_newlines=False)

      # Return the output of the process to the caller
      return completed.returncode, completed.stdout, completed.stderr

    # We catch xecutionerror, but continue execution and return completed structure to the caller
    # It has to be done since we execute tests that can fail. Thus global execution hould not stop
    # on first error
    except subprocess.CalledProcessError as exception:
      # Return the output of the process to the caller
      return exception.returncode, exception.stdout.decode(Key.UTF8.value), \
             exception.stderr.decode(Key.UTF8.value)
