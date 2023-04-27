# File for the 2nd project to IPP university class.
# Author: Anastasiia Berezovska xberez04@stud.fit.vutbr.cz

import re
import sys

from lib.Instruction import Instruction
from lib.error_code import *
import lib.error_code as E
from lib.Frame import Frame
from lib.Argument import Argument


# Class represents execution of program where all instructions are processed.
class Execution:

    data_stack = list()
    frame = Frame()
    labels = list()

    def __init__(self):
        pass

    # Instruction processing
    def execute(self, list_inst):

        for key in list_inst:

            key_get = key[0]
            name = key[0]
            i_name = name[:-2]
            new_key = key[0]
            key_for_function = new_key.split()[0]
            new_key = new_key.replace(" ", "")  # Removes whitespaces from keys to use it in match()
            i = Instruction(i_name, list_inst, None, None, None)
            unordered_arg_list = i.get_inst_args_list(key_get)  # list of instruction args
            # new_arg_list = i.remove_whitespaces(unordered_arg_list)     # new list of args with removed whitespaces
            cnt = len(unordered_arg_list)
            ordered_arg_list = i.order_inst_args(unordered_arg_list)  # new list of args with ordered args
            Instruction.check_count_args(key_for_function, cnt)

            if re.match('(MOVE)', new_key):  # MOVE <var> <symb>
                i.arg1, i.arg2 = i.define_args(ordered_arg_list, 2)
                if len(i.arg1) == 3:
                    i.arg1, i.arg2 = i.set_args(2, i)  # set type and value of argument
                else:
                    i.arg1 = Argument(i.arg1[1], i.arg1[2])
                    i.arg2 = Argument(i.arg2[0], i.arg2[1])
                self.frame.check_var_type_and_frame(i)

                if i.arg2.type == 'var':
                    var_type, var_value = self.frame.set_type_and_value(i, 2)
                else:
                    var_type, var_value = i.arg2.type, i.arg2.value

                if i.arg2.type != 'string' and i.arg2.value is None:
                    E.exit_code('Error! Argument value is missing\n', WRONG_STRING_WORK)  # Error 58

                self.frame.set_var(i.arg1, var_type, var_value)

            elif re.match('(CREATEFRAME)', new_key):  # CREATEFRAME
                self.frame.create_frame()

            elif re.match('(PUSHFRAME)', new_key):  # PUSHFRAME
                self.frame.push_frame()

            elif re.match('(POPFRAME)', new_key):  # POPFRAME
                self.frame.pop_frame()

            elif re.match('(DEFVAR)', new_key):  # DEFVAR <var>
                i.arg1 = i.define_args(ordered_arg_list, 1)
                i.arg1 = i.set_args(1, i)
                Instruction.check_var_type(i.arg1.type, 'var')
                self.frame.def_var(i.arg1)

            elif re.match('(PUSHS)', new_key):  # PUSHS <symb>
                i.arg1 = i.define_args(ordered_arg_list, 1)
                i.arg1 = i.set_args(1, i)

                if i.arg1.type == 'var':
                    first_typ, first_value = self.frame.set_type_and_value(i, 1)
                else:
                    first_typ, first_value = i.arg1.type, i.arg1.value

                self.data_stack.append((first_typ, first_value))

            elif re.match('(POPS)', new_key):  # POPS <var>
                i.arg1 = i.define_args(ordered_arg_list, 1)
                i.arg1 = i.set_args(1, i)

                if len(self.data_stack) == 0:
                    E.exit_code('Error! Data stack is empty!\n', MISSING_VALUE)  # Error 56

                data_stack_value = self.data_stack[-1]
                typ, value = data_stack_value[0], data_stack_value[1]
                self.frame.set_var(i.arg1, typ, value)

            elif re.match('(ADD|SUB|MUL|IDIV)', new_key):  # ADD <var> <symb1> <symb2>
                i.arg1, i.arg2, i.arg3 = i.define_args(ordered_arg_list, 3)
                i.arg1, i.arg2, i.arg3 = i.set_args(3, i)  # set type and value of argument
                self.frame.check_var_type_and_frame(i)

                i.arg2.type, i.arg2.value = self.frame.check_type(i.arg2)
                i.arg3.type, i.arg3.value = self.frame.check_type(i.arg3)

                if i.arg2.type != 'int' or i.arg3.type != 'int':
                    E.exit_code("Error! Wrong type of argument\n", WRONG_OPERAND_TYPES)  # Error 53

                if i.arg2.value[0] == '-' or i.arg3.value[0] == '-':  # check negative numbers
                    value_without_minus_2 = i.arg2.value[1:]
                    value_without_minus_3 = i.arg3.value[1:]

                    if value_without_minus_2.isdigit() and value_without_minus_3.isdigit():
                        pass
                    else:
                        E.exit_code("Error! Wrong argument value\n", UNEXPECTED_XML_STRUCTURE)  # Error 32

                elif not (i.arg2.value.isdigit() and i.arg3.value.isdigit()):
                    E.exit_code('Error! Wrong argument value\n', UNEXPECTED_XML_STRUCTURE)  # Error 32

                if re.match('(ADD)', new_key):
                    result = str(int(i.arg2.value) + int(i.arg3.value))
                elif re.match('(SUB)', new_key):
                    result = str(int(i.arg2.value) - int(i.arg3.value))
                elif re.match('(MUL)', new_key):
                    result = str(int(i.arg2.value) * int(i.arg3.value))
                else:
                    if i.arg3.value == '0':
                        E.exit_code('Error! Division by 0 is not possible\n', BAD_OPERAND_VALUE)  # Error 57
                    result = str(int(i.arg2.value) / int(i.arg3.value))

                self.frame.set_var(i.arg1, 'int', result)

            elif re.match('(LT|GT|EQ)', new_key):
                i.arg1, i.arg2, i.arg3 = i.define_args(ordered_arg_list, 3)
                i.arg1, i.arg2, i.arg3 = i.set_args(3, i)
                self.frame.check_var_type_and_frame(i)

                if i.arg2.type == 'var':
                    second_typ, second_value = self.frame.set_type_and_value(i, 2)
                else:
                    second_typ, second_value = i.arg2.type, i.arg2.value

                if i.arg3.type == 'var':
                    third_typ, third_value = self.frame.set_type_and_value(i, 3)
                else:
                    third_typ, third_value = i.arg3.type, i.arg3.value

                if re.match('(LT|GT)', new_key):
                    if second_typ == 'nil' or third_typ == 'nil':
                        E.exit_code('Wrong argument type\n', WRONG_OPERAND_TYPES)  # Error 53

                    if second_typ != third_typ:
                        E.exit_code('Wrong argument type\n', WRONG_OPERAND_TYPES)  # Error 53

                    if re.match('(LT)', new_key):
                        result = second_value < third_value
                    else:
                        result = second_value > third_value

                if re.match('(EQ)', new_key):
                    if second_typ == 'nil' or third_typ == 'nil':
                        result = second_value == third_value
                    elif second_typ == third_typ:
                        result = second_value == third_value
                    else:
                        E.exit_code('Error! Wrong argument type\n', WRONG_OPERAND_TYPES)  # Error 53

                result = i.bool_to_str(result)

                self.frame.set_var(i.arg1, 'bool', result)

            elif re.match('(AND|OR)', new_key):  # ADD/OR <var> <symb1> <symb2>
                i.arg1, i.arg2, i.arg3 = i.define_args(ordered_arg_list, 3)
                i.arg1, i.arg2, i.arg3 = i.set_args(3, i)
                self.frame.check_var_type_and_frame(i)

                if (i.arg2.type == 'bool' or i.arg2.type == 'var') and (i.arg3.type == 'bool' or i.arg3.type == 'var'):
                    pass
                else:
                    E.exit_code('Error! Wrong argument type\n', WRONG_OPERAND_TYPES)  # Error 53

                if i.arg2.type == 'var':
                    self.frame.check_variable_in_frame(i.arg2)
                    second_typ, second_value = self.frame.check_type(i.arg2)
                    if second_typ == 'bool' or second_typ == 'var':
                        pass
                    else:
                        E.exit_code('Error! Wrong argument type\n', WRONG_OPERAND_TYPES)  # Error 53
                else:
                    second_typ, second_value = i.arg2.type, i.arg2.value

                if i.arg3.type == 'var':
                    self.frame.check_variable_in_frame(i.arg3)
                    third_typ, third_value = self.frame.check_type(i.arg3)
                    if third_typ == 'bool' or third_typ == 'var':
                        pass
                    else:
                        E.exit_code('Error! Wrong argument type\n', WRONG_OPERAND_TYPES)  # Error 53
                else:
                    third_typ, third_value = i.arg3.type, i.arg3.value

                if second_value is None or third_value is None:
                    E.exit_code('Wrong argument value (is empty)\n', MISSING_VALUE)  # Error 56

                second_value = Instruction.str_to_bool(second_value)
                third_value = Instruction.str_to_bool(third_value)

                if re.match('(AND)', new_key):
                    result = second_value and third_value  # AND
                    result = Instruction.bool_to_str(result)
                else:
                    result = second_value or third_value  # OR
                    result = Instruction.bool_to_str(result)

                self.frame.set_var(i.arg1, 'bool', result)

            elif re.match('(NOT)', new_key):  # NOT <var> <symb>
                i.arg1, i.arg2 = i.define_args(ordered_arg_list, 2)
                i.arg1, i.arg2 = i.set_args(2, i)
                self.frame.check_var_type_and_frame(i)

                if i.arg2.type == 'bool' or i.arg2.type == 'var':
                    pass
                else:
                    E.exit_code('Error! Wrong argument type\n', WRONG_OPERAND_TYPES)  # Error 53

                if i.arg2.type == 'var':
                    self.frame.check_variable_in_frame(i.arg2)
                    second_typ, second_value = self.frame.check_type(i.arg2)
                    if second_typ == 'bool' or second_typ == 'var':
                        pass
                    else:
                        E.exit_code('Error! Wrong argument type\n', WRONG_OPERAND_TYPES)  # Error 53
                else:
                    second_typ, second_value = i.arg2.type, i.arg2.value

                if second_value is None:
                    E.exit_code('Wrong argument value (is empty)\n', MISSING_VALUE)  # Error 56

                second_value = Instruction.str_to_bool(second_value)
                result = i.not_bool_to_str(second_value)

                self.frame.set_var(i.arg1, 'bool', result)

            elif re.match('(INT2CHAR)', new_key):  # INT2CHAR <var> <symb>
                i.arg1, i.arg2 = i.define_args(ordered_arg_list, 2)
                i.arg1, i.arg2 = i.set_args(2, i)

                self.frame.check_var_type_and_frame(i)

                if i.arg2.type == 'var':
                    typ, value = self.frame.set_type_and_value(i, 2)
                else:
                    typ, value = i.arg2.type, i.arg2.value

                if typ != 'int':
                    E.exit_code('Error! Wrong argument value\n', WRONG_OPERAND_TYPES)  # Error 56

                if int(value) > 256 or int(value) < 0:
                    E.exit_code('Error! Wrong argument value\n', WRONG_STRING_WORK)  # Error 58

                ascii_code = chr(int(value))

                if not (0 <= int(ord(ascii_code)) <= 255):
                    E.exit_code('Error! Invalid symbol\n', WRONG_STRING_WORK)  # Error 58

                self.frame.set_var(i.arg1, 'var', ascii_code)

            elif re.match('(STRI2INT)', new_key):  # STRI2INT <var> <symb1> <symb2>
                i.arg1, i.arg2, i.arg3 = i.define_args(ordered_arg_list, 3)

                i.arg1, i.arg2, i.arg3 = i.set_args(3, i)
                if i.check_var_type(i.arg1.type, 'var'):
                    self.frame.check_variable_in_frame(i.arg1)

                if i.arg2.type == 'var':
                    second_typ, second_value = self.frame.set_type_and_value(i, 2)
                else:
                    second_typ, second_value = i.arg2.type, i.arg2.value

                if i.arg3.type == 'var':
                    third_typ, third_value = self.frame.set_type_and_value(i, 3)
                else:
                    third_typ, third_value = i.arg3.type, i.arg3.value

                if third_typ == 'nil' or third_typ == 'bool':
                    E.exit_code('Error! Wrong argument type\n', WRONG_OPERAND_TYPES)  # Error 53

                if not third_value.isnumeric():
                    E.exit_code('Error! Wrong argument value\n', WRONG_OPERAND_TYPES)  # Error 53

                index = int(third_value)

                if index not in range(len(second_value)):
                    E.exit_code('Error! Index is out of range\n',
                                WRONG_OPERAND_TYPES)  # Error 53 todo: MUST BE ERROR 58 ???

                str_symbol = second_value[index]
                ascii_code = ord(str_symbol)

                self.frame.set_var(i.arg1, 'int', ascii_code)

            elif re.match('(WRITE)', new_key):  # WRITE <symb>
                i.arg1 = i.define_args(ordered_arg_list, 1)
                i.arg1 = i.set_args(1, i)

                if i.arg1.type == 'var':
                    first_typ, first_value = self.frame.set_type_and_value(i, 1)
                else:
                    first_typ, first_value = i.arg1.type, i.arg1.value

                if first_value is None:
                    E.exit_code('Error! Argument value is missing\n', MISSING_VALUE)  # Error 56
                else:
                    print("" if first_typ == 'nil' else first_value, end='', file=sys.stdout)

            elif re.match('(CONCAT)', new_key):  # CONCAT <var> <symb1> <symb2>
                i.arg1, i.arg2, i.arg3 = i.define_args(ordered_arg_list, 3)
                i.arg1, i.arg2, i.arg3 = i.set_args(3, i)

                i.check_var_type(i.arg1.type, 'var')

                if i.arg2.type == 'var':
                    second_typ, second_value = self.frame.set_type_and_value(i, 2)
                else:
                    second_value = i.arg2.value
                    second_typ = i.arg2.type

                if second_typ != 'string':
                    E.exit_code('Error! Wrong argument type\n', WRONG_OPERAND_TYPES)  # Error 53

                if i.arg3.type == 'var':
                    third_typ, third_value = self.frame.set_type_and_value(i, 3)
                else:
                    third_typ, third_value = i.arg3.type, i.arg3.value

                if third_typ != 'string':
                    E.exit_code('Error! Wrong argument type\n', WRONG_OPERAND_TYPES)  # Error 53

                concat_str = str(second_value) + str(third_value)

                self.frame.set_var(i.arg1, 'string', concat_str)

            elif re.match('(STRLEN)', new_key):  # STRLEN <var> <symb>
                i.arg1, i.arg2 = i.define_args(ordered_arg_list, 2)
                i.arg1, i.arg2 = i.set_args(2, i)
                i.check_var_type(i.arg1.type, 'var')

                if i.arg2.type == 'var':
                    self.frame.check_variable_in_frame(i.arg2)
                typ, value = self.frame.check_type(i.arg2)

                if typ != 'string':
                    E.exit_code('Error! Wrong type of argument value\n', WRONG_OPERAND_TYPES)
                else:
                    length = len(str(value))

                self.frame.set_var(i.arg1, typ, length)

            elif re.match('(GETCHAR)', new_key):  # GETCHAR <var> <symb1> <symb2>
                i.arg1, i.arg2, i.arg3 = i.define_args(ordered_arg_list, 3)
                i.arg1, i.arg2, i.arg3 = i.set_args(3, i)  # set type and value of args
                i.check_var_type(i.arg1.type, 'var')

                if i.arg2.type == 'var':
                    second_typ, second_value = self.frame.set_type_and_value(i, 2)
                else:
                    second_typ, second_value = i.arg2.type, i.arg2.value

                if i.arg3.type == 'var':
                    third_typ, third_value = self.frame.set_type_and_value(i, 3)
                else:
                    third_typ, third_value = i.arg3.type, i.arg3.value

                if third_typ == 'nil' or third_typ == 'bool':
                    E.exit_code('Error! Wrong argument type', WRONG_OPERAND_TYPES)  # Error 53

                if not third_value.isnumeric():
                    E.exit_code('Error! Wrong argument value\n', WRONG_OPERAND_TYPES)  # Error 53

                index = int(third_value)

                if index not in range(len(second_value)):
                    E.exit_code('Error! Index is out of range\n',
                                WRONG_OPERAND_TYPES)  # Error 53 todo: MUST BE ERROR 58 ???

                str_symbol = second_value[index]

                self.frame.set_var(i.arg1, second_typ, str_symbol)

            elif re.match('(SETCHAR)', new_key):  # SETCHAR <var> <symb1> <symb2>
                i.arg1, i.arg2, i.arg3 = i.define_args(ordered_arg_list, 3)
                i.arg1, i.arg2, i.arg3 = i.set_args(3, i)  # set type and value of args

                i.check_var_type(i.arg1.type, 'var')
                first_typ, first_value = self.frame.set_type_and_value(i, 1)

                if i.arg2.type == 'var':
                    second_typ, second_value = self.frame.set_type_and_value(i, 2)
                else:
                    second_typ, second_value = i.arg2.type, i.arg2.value

                if i.arg3.type == 'var':
                    third_typ, third_value = self.frame.set_type_and_value(i, 3)
                else:
                    third_typ, third_value = i.arg3.type, i.arg3.value

                if second_typ == 'nil' or second_typ == 'bool':
                    E.exit_code('Error! Wrong argument type', WRONG_OPERAND_TYPES)  # Error 53

                if not second_value.isnumeric():
                    E.exit_code('Error! Wrong argument value\n', WRONG_OPERAND_TYPES)  # Error 53

                if third_typ == 'string' and third_value == '':
                    E.exit_code('Error! Wrong argument value\n', WRONG_STRING_WORK)  # Error 58

                index = int(second_value)

                if index not in range(len(first_value)):
                    E.exit_code('Error! Index is out of range\n', WRONG_OPERAND_TYPES)  # Error 53

                char_to_change = first_value[index]
                changed_value = first_value.replace(char_to_change, third_value[0])

                self.frame.set_var(i.arg1, first_value, changed_value)

            elif re.match('(TYPE)', new_key):  # TYPE <var> <symb>
                i.arg1, i.arg2 = i.define_args(ordered_arg_list, 2)
                i.arg1, i.arg2 = i.set_args(2, i)  # set type and value of args

                i.check_var_type(i.arg1.type, 'var')
                first_typ, first_value = self.frame.set_type_and_value(i, 1)

                if i.arg2.type == 'var':
                    second_typ, second_value = self.frame.set_type_and_value(i, 2)
                else:
                    second_typ, second_value = i.arg2.type, i.arg2.value

                if second_typ is None:
                    second_typ = ''

                self.frame.set_var(i.arg1, i.arg1.type, second_typ)

            elif re.match('(DPRINT)', new_key): # DPRINTF <symb>
                i.arg1 = i.define_args(ordered_arg_list, 1)
                i.arg1 = i.set_args(1, i)

                if i.arg1.type == 'var':
                    typ, value = self.frame.set_type_and_value(i, 1)
                else:
                    typ, value = i.arg1.type, i.arg1.value

                sys.stderr.write(value)

            elif re.match('(BREAK)', new_key):
                sys.stderr.write('Frames content: GF: ' + str(self.frame.Frames[0]) + ' LF: ' + str(self.frame.Frames[1]) + ' TF: ' + str(self.frame.Frames[2]) + '\n')

            elif re.match('EXIT', new_key):
                i.arg1 = i.define_args(ordered_arg_list, 1)
                i.arg1 = i.set_args(1, i)

                if i.arg1.type == 'var':
                    typ, value = self.frame.set_type_and_value(i, 1)
                else:
                    typ, value = i.arg1.type, i.arg1.value

                if int(value) < 0 or int(value) > 49:
                    E.exit_code('Error! Wrong error code value\n', BAD_OPERAND_VALUE)   # Error 57

                E.exit_code('Exit instruction\n', int(value))

            elif re.match('(LABEL)', new_key):  # LABEL <label>
                i.arg1 = i.define_args(ordered_arg_list, 1)
                i.arg1 = i.set_args(1, i)

                if i.arg1.type == 'label':
                    if i.arg1.value in self.labels:
                        E.exit_code('Error! Wrong argument type\n', SEMANTIC_ERROR)  # Error 52
                    else:
                        self.labels.append(i.arg1.value)
                else:
                    E.exit_code('Error! Wrong argument type\n', WRONG_OPERAND_TYPES)  # Error 53

            elif re.match('(JUMPIFEQ)', new_key):  # JUMPIFEQ <label> <symb1> <symb2>
                i.arg1, i.arg2, i.arg3 = i.define_args(ordered_arg_list, 3)
                i.arg1, i.arg2, i.arg3 = i.set_args(3, i)

                i.check_var_type(i.arg1.type, 'label')

                if (i.arg2.type == i.arg3.type) or (i.arg2.type == 'nil' or i.arg3.type == 'nil'):
                    if i.arg2.type == 'var' and i.arg3.type == 'var':
                        second_typ, second_value = self.frame.set_type_and_value(i, 2)
                        third_typ, third_value = self.frame.set_type_and_value(i, 3)
                        if (second_typ == third_typ) or (second_typ == 'nil' or third_typ == 'nil'):
                            pass
                        else:
                            E.exit_code('Error! Wrong argument type\n', WRONG_OPERAND_TYPES)

                    else:
                        second_value, third_value = i.arg2.value, i.arg3.value

                    if second_value == third_value:
                        pass
                    # todo provede skok na label
                    else:
                        E.exit_code('Error! Wrong argument type\n', WRONG_OPERAND_TYPES)
                else:
                    E.exit_code('Error! Wrong argument type\n', WRONG_OPERAND_TYPES)  # Error 53

            else:
                pass
        pass
