# File for the 2nd project to IPP university class.
# Author: Anastasiia Berezovska xberez04@stud.fit.vutbr.cz

from lib.error_code import *
import lib.error_code as E
from lib.Instruction import *


# Class Frame represents dictionary that stores variable and its value.
# Attributes: GF - for storing global vars, LF - for storing local vars,
#             TF - for preparing new or tidying up an old frame.
class Frame:
    GF = {}
    LF = []
    TF = None
    Frames = [GF,  # Frame[0]
              LF,  # Frame[1]
              TF]  # Frame[2]

    def __init__(self):
        self._temporaryFrameDefined = False

    def create_frame(self):
        self.Frames[2] = {}
        self._temporaryFrameDefined = True

    def is_empty_frame(self):
        return len(self.Frames[1]) == 0

    def push_frame(self):
        if self._temporaryFrameDefined:
            self.Frames[1].append(self.Frames[2])
            self.Frames[2] = None
            self._temporaryFrameDefined = False
        else:
            E.exit_code('Error! Pushframe cannot execute with undefined frame\n', FRAME_DOES_NOT_EXIST)  # Error 55

    def pop_frame(self):
        if self.is_empty_frame():
            E.exit_code('Error! Popframe cannot execute with empty stack\n', FRAME_DOES_NOT_EXIST)  # Error 55

        else:
            self.Frames[2] = self.Frames[1].pop()
            self._temporaryFrameDefined = True

    def top_frame(self):
        if len(self.Frames[1]) == 0:
            return "Frame stack is empty"
        return self.Frames[1][0]  # 1st item from LF

    # Returns content of current frame
    def get_frame(self, frame: str):
        if frame == 'GF':
            return self.Frames[0]
        elif frame == 'LF':
            if not self.is_empty_frame():
                return self.Frames[1][-1]  # last item from LF
            else:   # if stack is empty
                return None
        elif frame == 'TF':
            if self._temporaryFrameDefined:
                return self.Frames[2]
            else:
                return None

    # Checks if current variable is in certain frame
    def check_variable_in_frame(self, arg: Argument):
        frame, name = arg.value.split('@')
        frame_obj = self.get_frame(frame)
        if name in frame_obj:
            pass
        else:
            E.exit_code('Error! Variable is not declared, access to non-existent var\n', ACCESS_TO_NON_EXISTENT_VAR)

    def check_type(self, arg: Argument):
        if arg.type == 'var':
            temp = self.get_variable(arg)
            if temp is None:
                E.exit_code('Error! Variable value is empty\n', MISSING_VALUE)  # Error 56
            typ = temp['type']
            value = temp['value']
        else:
            typ, value = arg.type, arg.value
        return typ, value

    # Defines variable
    def def_var(self, arg: Argument):
        frame, name = arg.value.split('@')
        frame_obj = self.get_frame(frame)
        if frame_obj is None:
            E.exit_code('Error! Variable declaration in undefined frame is not possible\n',
                        FRAME_DOES_NOT_EXIST)  # Error 58
        else:
            if name is None:
                E.exit_code('Error! Variable name is not defined\n',
                            SEMANTIC_ERROR)  # Error code for undefined variable
            elif name in frame_obj:
                E.exit_code('Error! Variable redefinition is not possible\n', SEMANTIC_ERROR)  # Error 52
            else:
                frame_obj[name] = {'type': None, 'value': None}

    # Sets var type and value
    def set_var(self, arg, typ: str, value):
        frame, name = arg.value.split('@')
        frame_obj = self.get_frame(frame)
        if frame_obj is None:
            E.exit_code('Error! Reading variable from undefined frame\n', FRAME_DOES_NOT_EXIST)  # Error 55
        if name not in frame_obj:
            E.exit_code('Error! Impossible to write into non-existing variable\n',
                        ACCESS_TO_NON_EXISTENT_VAR)  # Error 54
        frame_obj[name]['type'] = typ
        frame_obj[name]['value'] = value

    # Get variable from frame
    def get_variable(self, arg):
        frame, name = arg.value.split('@')
        frame_obj = self.get_frame(frame)
        if name not in frame_obj:
            E.exit_code('Error! Undeclared variable\n', ACCESS_TO_NON_EXISTENT_VAR)
        else:
            pass
        return frame_obj[name]

    def check_var_type_and_frame(self, inst):
        inst.check_var_type(inst.arg1.type, 'var')
        self.check_variable_in_frame(inst.arg1)

    # Sets variable type and value
    def set_type_and_value(self, inst: Instruction, number_of_arg):
        if number_of_arg == 1:
            self.check_variable_in_frame(inst.arg1)
            var = self.get_variable(inst.arg1)
            var_type = var['type']
            var_value = var['value']

            return var_type, var_value

        elif number_of_arg == 2:
            self.check_variable_in_frame(inst.arg2)
            var = self.get_variable(inst.arg2)
            var_type = var['type']
            var_value = var['value']

            return var_type, var_value

        elif number_of_arg == 3:
            self.check_variable_in_frame(inst.arg3)
            var = self.get_variable(inst.arg3)
            var_type = var['type']
            var_value = var['value']

            return var_type, var_value
