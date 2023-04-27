# File for the 2nd project to IPP university class.
# Author: Anastasiia Berezovska xberez04@stud.fit.vutbr.cz

import sys

SUCCESS = 0
MISSING_OR_BAD_PARAM = 10
OPEN_INPUT_FILE_ERROR = 11
OPEN_OUTPUT_FILE_ERROR = 12
BAD_XML_FORMAT = 31
UNEXPECTED_XML_STRUCTURE = 32
SEMANTIC_ERROR = 52                 # e.g. the use of undefined label, redefinition of the variable
WRONG_OPERAND_TYPES = 53
ACCESS_TO_NON_EXISTENT_VAR = 54      # Frame exists
FRAME_DOES_NOT_EXIST = 55           # E.g. reading from an empty frame stack
MISSING_VALUE = 56                  # In a variable, on a data stack, or in the call stack
BAD_OPERAND_VALUE = 57              # E.g. division by zero, bad returns value of the EXIT instruction
WRONG_STRING_WORK = 58
INTERNAL_ERROR = 99


def exit_code(error_msg: str, error_code: int):
    sys.stderr.write(error_msg)
    exit(error_code)
