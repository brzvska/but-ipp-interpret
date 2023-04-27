# File for the 2nd project to IPP university class.
# Author: Anastasiia Berezovska xberez04@stud.fit.vutbr.cz
import sys

from lib.error_code import *
import lib.error_code as E
from lib.Argument import Argument

inst_params = {"MOVE": 2,
               "CREATEFRAME": 0,
               "PUSHFRAME": 0,
               "POPFRAME": 0,
               "DEFVAR": 1,
               "CALL": 1,
               "RETURN": 0,
               "PUSHS": 1,
               "POPS": 1,
               "ADD": 3,
               "SUB": 3,
               "MUL": 3,
               "IDIV": 3,
               "LT": 3,
               "GT": 3,
               "EQ": 3,
               "AND": 3,
               "OR": 3,
               "NOT": 2,
               "INT2CHAR": 2,
               "STRI2INT": 3,
               "READ": 2,
               "WRITE": 1,
               "CONCAT": 3,
               "STRLEN": 2,
               "GETCHAR": 3,
               "SETCHAR": 3,
               "TYPE": 2,
               "LABEL": 1,
               "JUMP": 1,
               "JUMPIFEQ": 3,
               "JUMPIFNEQ": 3,
               "EXIT": 1,
               "DPRINT": 1,
               "BREAK": 0
               }


# Class Instruction represents IPPcode23 instruction.
# Attributes: name - instruction opcode, number - instruction order,
#             args - list of instruction arguments (if it has some).

class Instruction:
    instruction_list = []
    instructions_dict = {}
    arguments = {}

    def __init__(self, name: str, dict_args, arg1: Argument, arg2: Argument, arg3: Argument):
        self.instruction_list.append(self)
        self.name = name
        self.arguments_dict: dict() = dict_args
        self.arg1 = None
        self.arg2 = None
        self.arg3 = None

    def get_inst_args_list(self, key_name: str):
        x = self.instructions_dict.get(key_name)
        return x

    def define_args(self, ordered_list, number):
        if number == 1:
            self.arg1 = ordered_list[0]

            return self.arg1

        elif number == 2:
            self.arg1 = ordered_list[0]
            self.arg2 = ordered_list[1]

            return self.arg1, self.arg2

        else:
            self.arg1 = ordered_list[0]
            self.arg2 = ordered_list[1]
            self.arg3 = ordered_list[2]

            return self.arg1, self.arg2, self.arg3

    @staticmethod
    def set_args(number_og_args: int, instruction):
        if number_og_args == 1:
            argument_1 = Argument(instruction.arg1[0], instruction.arg1[1])

            return argument_1
        elif number_og_args == 2:
            argument_1 = Argument(instruction.arg1[0], instruction.arg1[1])
            argument_2 = Argument(instruction.arg2[1], instruction.arg2[2])

            return argument_1, argument_2
        else:
            argument_1 = Argument(instruction.arg1[0], instruction.arg1[1])  # TODO CHECK
            argument_2 = Argument(instruction.arg2[1], instruction.arg2[2])
            argument_3 = Argument(instruction.arg3[1], instruction.arg3[2])

            return argument_1, argument_2, argument_3

    @staticmethod
    def check_count_args(key, number):
        if number == inst_params[key]:
            return True
        else:
            E.exit_code('Error! Number of args is not correct ' + key + '\n', UNEXPECTED_XML_STRUCTURE)  # Error 32

    @staticmethod
    def check_var_type(current_type: str, correct_type: str):
        if current_type != correct_type:
            E.exit_code('Error! Wrong type of argument\n', WRONG_OPERAND_TYPES)  # Error 53
        else:
            pass

    @staticmethod
    # Orders arguments in right order
    def order_inst_args(args: list):
        sorted_arg_list = sorted(args, key=lambda x: x[-1][-1])
        return sorted_arg_list

    # Removes whitespaces and new lines from items in tuples in list of arguments.
    # @staticmethod
    # def remove_whitespaces(args_list: list):
    #     cleaned_lst = []
    #     for tup in args_list:
    #         cleaned_tup = tuple(val.strip() for val in tup if val is not None)
    #         cleaned_lst.append(cleaned_tup)
    #     return cleaned_lst

    @staticmethod
    def str_to_bool(value) -> bool:
        if value == 'true':
            return True
        else:
            return False

    @staticmethod
    def bool_to_str(value) -> str:
        if value is True:
            return 'true'
        else:
            return 'false'

    @staticmethod
    def not_bool_to_str(value) -> str:
        if value is True:
            return 'false'
        else:
            return 'true'
