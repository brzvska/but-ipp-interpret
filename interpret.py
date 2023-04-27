# File for the 2nd project to IPP university class.
# Author: Anastasiia Berezovska xberez04@stud.fit.vutbr.cz

import re
import xml.etree.ElementTree as ET
from lib.Instruction import Instruction
from lib.error_code import *
import lib.error_code as E
from lib.XMLParser import XMLParser
from lib.Frame import Frame
from lib.Execution import Execution


# Checks xml structure.
def check_xml(file):
    try:
        etree = ET.parse(file)
    except ET.ParseError:
        E.exit_code('Error! ParseError\n', BAD_XML_FORMAT)  # Error 31
    return etree


# Prints helping message in case there is --help parameter.
def print_help_message() -> None:
    if len(sys.argv) != 2:
        E.exit_code('Error! Missing or bad parameter\n', MISSING_OR_BAD_PARAM)  # Error 10

    print("Usage: python3.10 interpret.py [--help] [--source=file] [--input=file]")
    print("Options and arguments:")
    print("\t--help          prints help message to standart output")
    print("\t--source=file   file with source XML code")
    print("\t--input=file    file with source code for instruction READ\n")
    E.exit_code('OK\n', SUCCESS)


# ---------------------------------------   Arguments parsing   --------------------------------------------------------
if len(sys.argv) > 3 or len(sys.argv) < 1:
    E.exit_code('Error! Missing or bad parameter\n', MISSING_OR_BAD_PARAM)  # Error 10

for arg in sys.argv[1:]:
    if arg == '--help' or arg == '-h':
        print_help_message()

    elif arg.startswith('--source='):
        source_file = arg[9:]

    elif arg.startswith('--input='):
        input_file = arg[8:]

    else:
        E.exit_code('Error! Missing or bad parameter.\n', MISSING_OR_BAD_PARAM)  # Error 10

# ----------------------------------------------------------------------------------------------------------------------
instruction_obj = Instruction
# ----------------------------------------   XML loading   -------------------------------------------------------------
xml_parser = XMLParser()
try:
    source_file = open(source_file, "r")
except FileNotFoundError:
    E.exit_code('Error! FileNotFoundError\n', MISSING_OR_BAD_PARAM)  # Error 10

tree = check_xml(source_file)
xml_parser.parse(tree)
list_inst = xml_parser.get_dict_ordered(instruction_obj.instructions_dict)  # dictionary of instructions

# ---------------------------------------   Execution ------------------------------------------------------------------
execution = Execution()
execution.execute(list_inst)    # main program execution
