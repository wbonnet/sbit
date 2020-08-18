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


""" This modules defines ANSI code used to produce colored output in shell.
"""

from enum import Enum

# -----------------------------------------------------------------------------
#
# class Colors
#
# -----------------------------------------------------------------------------
class Colors(Enum):
  """This class defines the ANSI code used to control the colors (backgrouond
  and foreground) of the characters when output in a shell.
  """

  # Control codes
  RESET = "\033[0m"
  BOLD = "\033[01m"
  DISABLE = "\033[02m"
  UNDERLINE = "\033[04m"
  REVERSE = "\033[07m"
  STRIKETHROUGH = "\033[09m"
  INVISIBLE = "\033[08m"

  # Foreground color control
  FG_BLACK = "\033[30m"
  FG_RED = "\033[31m"
  FG_GREEN = "\033[32m"
  FG_ORANGE = "\033[33m"
  FG_BLUE = "\033[34m"
  FG_PURPLE = "\033[35m"
  FG_CYAN = "\033[36m"
  FG_LIGHTGREY = "\033[37m"
  FG_DARKGREY = "\033[90m"
  FG_LIGHTRED = "\033[91m"
  FG_LIGHTGREEN = "\033[92m"
  FG_YELLOW = "\033[93m"
  FG_LIGHTBLUE = "\033[94m"
  FG_PINK = "\033[95m"
  FG_LIGHTCYAN = "\033[96m"

  # Background color control
  BG_BLACK = "\033[40m"
  BG_RED = "\033[41m"
  BG_GREEN = "\033[42m"
  BG_ORANGE = "\033[43m"
  BG_BLUE = "\033[44m"
  BG_PURPLE = "\033[45m"
  BG_CYAN = "\033[46m"
  BG_LIGHTGREY = "\033[47m"
