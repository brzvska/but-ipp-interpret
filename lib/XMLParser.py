# File for the 2nd project to IPP university class.
# Author: Anastasiia Berezovska xberez04@stud.fit.vutbr.cz
from lib.Instruction import *
import xml.etree.ElementTree as ET
from lib.error_code import *
import lib.error_code as E
import re


# Class XMLParser represents parser that parse xml file into instructions and its arguments.
# Attribute: instructions - list of instructions.
class XMLParser:
    def __init__(self):
        super().__init__()

    def parse(self, tree):

        self.check_tree(tree)
        root = tree.getroot()
        instruction_dict = Instruction.instructions_dict

        if root.tag != "program":
            E.exit_code("Error! root is not correct\n", UNEXPECTED_XML_STRUCTURE)  # Error 32

        if root.attrib['language'] != "IPPcode23":
            E.exit_code("Error! language is not correct\n", UNEXPECTED_XML_STRUCTURE)  # Error 32

        i_order = []

        for child in root:

            if child.tag != 'instruction':
                E.exit_code('Error! Wrong tag (must be instruction)\n', UNEXPECTED_XML_STRUCTURE)  # Error 32

            if (not child.attrib.get('order') or child.attrib['order'].isnumeric() is False) or (
            int(child.attrib['order'])) <= 0:
                E.exit_code("Error! Order is not a number or is missing\n", UNEXPECTED_XML_STRUCTURE)  # Error 32

            if not child.attrib.get('opcode'):
                E.exit_code("Error! Instruction opcode is missing\n", UNEXPECTED_XML_STRUCTURE)  # Error 32

            # Checks order duplicity
            if child.attrib['order'] in i_order:
                E.exit_code("Error! Duplicate order\n", UNEXPECTED_XML_STRUCTURE)  # Error 32

            i_order.append(child.attrib['order'])
            arg_order = []

            # Adds instructions without args to the instruction list
            key = str(child.attrib.get('opcode')) + ' ' + child.attrib['order']
            key.upper()
            if key not in instruction_dict:
                key_new = key.replace(" ", "")
                if re.match("CREATEFRAME|PUSHFRAME|POPFRAME|BREAK|RETURN", key_new):
                    instruction_dict[key] = []

            # Loop through "arg" of "instruction"
            for sub_elem in child:

                # Checks 'arg' in xml instructions
                if sub_elem.tag[0:3] != "arg" or int(sub_elem.tag[3:len(sub_elem.tag)]) > 3 or \
                        int(sub_elem.tag[3:len(sub_elem.tag)]) < 1:
                    E.exit_code("Error! Wrong argument\n", UNEXPECTED_XML_STRUCTURE)  # Error 32

                # Checks args order
                if sub_elem.tag[0:4] in arg_order:
                    E.exit_code("Error! Duplicate argument order", UNEXPECTED_XML_STRUCTURE)  # Error 32

                arg_order.append(sub_elem.tag[0:4])

                if 'type' not in sub_elem.attrib:
                    E.exit_code('Error! Attribute "type" is missing\n', UNEXPECTED_XML_STRUCTURE)

                if sub_elem.attrib['type'] not in ['string', 'bool', 'label', 'int', 'var', 'nil', 'type']:
                    E.exit_code('Error! Invalid argument type\n', UNEXPECTED_XML_STRUCTURE)

                if child.attrib['opcode'].upper() not in inst_params:
                    E.exit_code('Error! Wrong opcode ' + child.attrib['opcode'] + '\n', UNEXPECTED_XML_STRUCTURE)  # Error 32

                # Set the dictionary members (instructions with args)
                #       dictionary = { instruction : [(arg_type, arg_value)] }

                key = child.attrib['opcode'].upper() + ' ' + child.attrib['order']
                if key not in instruction_dict:
                    instruction_dict[key] = [(sub_elem.attrib['type'], sub_elem.text, sub_elem.tag)]    #TODO added tag
                else:
                    instruction_dict[key].append((child.attrib['order'], sub_elem.attrib['type'], sub_elem.text, sub_elem.tag))     #TODO added arg tag

            # Check arguments order (must start from 1)
            arg_help_list = [item[-1] for item in arg_order]
            l = len(arg_help_list)
            if l == 1:
                if '1' in arg_help_list:
                    pass
                else:
                    E.exit_code("Error! Wrong argument order (must be 1)\n", UNEXPECTED_XML_STRUCTURE)   # Error 32
            elif l == 2:
                if '1' in arg_help_list and '2' in arg_help_list:
                    pass
                else:
                    E.exit_code("Error! Wrong argument orders (must be 1, 2)\n", UNEXPECTED_XML_STRUCTURE)   # Error 32
            elif l == 3:
                if '1' in arg_help_list and '2' in arg_help_list and '3' in arg_help_list:
                    pass
                else:
                    E.exit_code("Error! Wrong argument orders (must be 1, 2, 3)\n", UNEXPECTED_XML_STRUCTURE)  # Error 32
            else:
                pass

    # for order in key
    @staticmethod
    def get_dict_ordered(_dict):
        sorted_list = sorted(_dict.items(), key=lambda x: int(x[0].split()[1]))
        return sorted_list

    @staticmethod
    def check_tree(tree):
        if tree is None:
            E.exit_code('Error! There is no xml tree\n', OPEN_INPUT_FILE_ERROR)     # Error 11
