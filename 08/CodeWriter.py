# rina.karnauch, came1337
# =============================================================================
# Rina Karnauch, rina.karnauch@mail.huji.ac.il
# Eynam Wassertheil, eynam.wassertheil@mail.huji.ac.il
# =============================================================================
from enum import Enum


class Segments(Enum):
    ARGUMENT = "argument"
    LOCAL = "local"
    STATIC = "static"
    CONSTANT = "constant"
    THIS = "this"
    THAT = "that"
    POINTER = "pointer"
    TEMP = "temp"


class Arithmetics(Enum):
    ADD = "add"
    SUB = "sub"
    NEG = "neg"
    EQ = "eq"
    GT = "gt"
    LT = "lt"
    AND = "and"
    OR = "or"
    NOT = "not"


LCL = "LCL"
ARG = "ARG"
THIS = "THIS"
THAT = "THAT"

CALL_DICTIONARY = [LCL, ARG, THIS, THAT]


class CodeWriter:
    # ------- helper methods ---------

    @staticmethod
    def get_segment_type(line: str):
        """
        method to get segment type, which stack to get or put from or into.
        :param line: push  or pop line without the "pop" or "push" command
        :return: segment type
        """
        for seg in Segments:
            if line.startswith(seg.value):
                return seg

    # ------- arithmetic methods ---------

    @staticmethod
    def arithmetic_line(counter: str, line: str):
        """
        method to convert an arithmetic line into an asm code
        :param counter: counter of line
        :param line: the line to convert from vm to asm
        :return: array of asm code lines
        """
        operator = line.strip()
        handling_method = CodeWriter.DICTIONARY.get(operator)
        lines = handling_method(counter)
        return lines

    @staticmethod
    def handle_add(counter: str):
        """
        method to handle arithmetic add line and turn it into an asm code
        :return: the asm array of add vm line
        """
        lines = ["@SP",  # eynam 15/11
                 "A=M",
                 "A=A-1",
                 "D=M",
                 "A=A-1",
                 "M=D+M",
                 "D=A+1",
                 "@SP",
                 "M=D"]
        return lines

    @staticmethod
    def handle_sub(counter: str):
        """
        method to handle arithmetic sub line and turn it into an asm code
        :return: the asm array of sub vm line
        """
        lines = ["@SP",  # eynam 15/11
                 "A=M",
                 "A=A-1",
                 "D=M",
                 "A=A-1",
                 "M=M-D",
                 "D=A+1",
                 "@SP",
                 "M=D"]
        return lines

    @staticmethod
    def handle_neg(counter: str):
        """
        method to handle arithmetic neg line and turn it into an asm code
        :return: the asm array of neg vm line
        """
        lines = ["@SP",
                 "A=M",
                 "A=A-1",
                 "M=-M"]
        return lines

    @staticmethod
    def handle_eq(counter: str):
        """
        method to handle arithmetic eq line and turn it into an asm code
        :return: the asm array of eq vm line
        """
        lines = ["@SP",
                 "M=M-1",
                 "A=M",
                 "D=M",
                 "@SP",
                 "A=M-1",
                 "D=M-D",
                 "@TRUE_EQ" + counter,
                 "D;JEQ",
                 "@SP",
                 "A=M-1",
                 "M=0",
                 "@END_EQ" + counter,
                 "0;JMP",
                 "(TRUE_EQ" + counter + ")",
                 "@SP",
                 "A=M-1",
                 "M=-1",
                 "(END_EQ" + counter + ")"]
        return lines

    @staticmethod
    def handle_gt(counter: str):
        """
        method to handle arithmetic gt line and turn it into an asm code
        :return: the asm array of gt vm line
        """
        lines = ["@SP",
                 "M=M-1",
                 "A=M",
                 "D=M",
                 "@R13",
                 "M=D",
                 "@R14",
                 "M=!D",
                 "@SP",
                 "A=M-1",
                 "D=M",
                 "@R13",
                 "M=M|D",
                 "@SP",
                 "A=M-1",
                 "D=!M",
                 "@R14",
                 "M=D|M",
                 "@R13",
                 "D=M",
                 "@R14",
                 "D=M&D",
                 "@DIFFSIGNS" + counter,
                 "D;JLT",
                 "@SP",
                 "A=M",
                 "D=M",
                 "@SP",
                 "A=M-1",
                 "D=M-D",
                 "(COMEBACK" + counter + ")",
                 "@GREATER" + counter,
                 "D;JGT",  # here
                 "D=0",
                 "@INSERT" + counter,
                 "0;JMP",
                 "(DIFFSIGNS" + counter + ")",
                 "@SP",
                 "A=M-1",
                 "D=M",
                 "@POSITIVE_FIRST" + counter,
                 "D;JGE",
                 "D=-1",
                 "@COMEBACK" + counter,
                 "0;JMP",
                 "(POSITIVE_FIRST" + counter + ")",
                 "D=1",
                 "@COMEBACK" + counter,
                 "0;JMP",
                 "(GREATER" + counter + ")",
                 "D=-1",
                 "(INSERT" + counter + ")",
                 "@SP",
                 "A=M-1",
                 "M=D"]
        return lines

    @staticmethod
    def handle_lt(counter: str):
        """
        method to handle arithmetic lt line and turn it into an asm code
        :return: the asm array of lt vm line
        """
        lines = ["@SP",
                 "M=M-1",
                 "A=M",
                 "D=M",
                 "@R13",
                 "M=D",
                 "@R14",
                 "M=!D",
                 "@SP",
                 "A=M-1",
                 "D=M",
                 "@R13",
                 "M=M|D",
                 "@SP",
                 "A=M-1",
                 "D=!M",
                 "@R14",
                 "M=D|M",
                 "@R13",
                 "D=M",
                 "@R14",
                 "D=M&D",
                 "@DIFFSIGNS" + counter,
                 "D;JLT",
                 "@SP",
                 "A=M",
                 "D=M",
                 "@SP",
                 "A=M-1",
                 "D=M-D",
                 "(COMEBACK" + counter + ")",
                 "@LOWER" + counter,
                 "D;JLT",
                 "D=0",
                 "@INSERT" + counter,
                 "0;JMP",
                 "(DIFFSIGNS" + counter + ")",
                 "@SP",
                 "A=M",
                 "D=M",
                 "@NEGATIVE_FIRST" + counter,
                 "D;JLT",
                 "D=-1",
                 "@COMEBACK" + counter,
                 "0;JMP",
                 "(NEGATIVE_FIRST" + counter + ")",
                 "D=1",
                 "@COMEBACK" + counter,
                 "0;JMP",
                 "(LOWER" + counter + ")",
                 "D=-1",
                 "(INSERT" + counter + ")",
                 "@SP",
                 "A=M-1",
                 "M=D"]
        return lines

    @staticmethod
    def handle_and(counter: str):
        lines = ["@SP",
                 "A=M",
                 "A=A-1",
                 "D=M",
                 "A=A-1",
                 "M=D&M",
                 "D=A+1",
                 "@SP",
                 "M=D"]
        return lines

    @staticmethod
    def handle_or(counter: str):
        lines = ["@SP",
                 "A=M",
                 "A=A-1",
                 "D=M",
                 "A=A-1",
                 "M=D|M",
                 "D=A+1",
                 "@SP",
                 "M=D"]
        return lines
        # print("hello")

    @staticmethod
    def handle_not(counter: str):
        """
        method to handle arithmetic not line and turn it into an asm code
        :return: the asm array of not vm line
        """
        lines = ["@SP",
                 "A=M",
                 "A=A-1",
                 "M=!M"]
        return lines

    # ------- push methods ---------

    @staticmethod
    def push_from_static(index: str, file_name: str):
        """
        push from constant into stack
        :param file_name: name of file we are at
        :param index: index to push
        :return: asm lines
        """
        lines = ["@" + file_name + "." + index,
                 "D=M",
                 "@SP",
                 "A=M",
                 "M=D",
                 "@SP",
                 "M=M+1"]
        return lines

    @staticmethod
    def push_constant(index: str):
        """
        push from constant into stack
        :param index: index to push
        :return: asm lines
        """
        lines = ["@" + index,
                 "D=A",
                 "@SP",
                 "A=M",
                 "M=D",
                 "@SP",
                 "M=M+1"]
        return lines

    @staticmethod
    def push_from_T(segment: str, index: str):
        """
        method to push to stack from local, this,that, argument stack
        :param segment: segment out of local, this,that, argument
        :param index: index to push from
        :return: asm lines of code of pushing
        """
        lines = ["@" + segment,
                 "D=M",
                 "@" + index,
                 "D=D+A",
                 "@R13",
                 "A=D",
                 "D=M",
                 "@SP",
                 "A=M",
                 "M=D",
                 "@SP",
                 "M=M+1"]
        return lines

    @staticmethod
    def push_from_temp(index: str):
        """
        method to push from temp to stack
        :param index: to push from temp
        :return: lines of asm code
        """
        lines = ["@R" + index,
                 "D=M",
                 "@SP",
                 "A=M",
                 "M=D",
                 "@SP",
                 "M=M+1"]
        return lines

    @staticmethod
    def push_from_pointer(index: str):
        """
        method to push from pointer to stack
        :param index: 0 or 1, to push from that(4) or from this(3)
        :return: lines of asm code
        """
        if index == "0":
            # this
            lines = ["@THIS"]
        else:

            # that
            lines = ["@THAT"]
        code = ["D=M",
                "@SP",
                "A=M",
                "M=D",
                "@SP",
                "M=M+1"]
        lines.extend(code)
        return lines

    @staticmethod
    def push_line(file_name: str, line: str):
        """
        method to convert a push line into an asm code
        :param file_name: file we are in to push into stack
        :param line: the line to convert from vm to asm
        :return: array of asm code lines
        """
        without_push = (line.split("push")[1]).strip()
        segment_type = CodeWriter.get_segment_type(without_push)
        index_of_segment = (line.split(segment_type.value)[1]).strip()

        segment_type = segment_type.value

        # push from constant:
        if segment_type == Segments.CONSTANT.value:
            lines = CodeWriter.push_constant(index_of_segment)
            return lines

        # push from local:
        elif segment_type == Segments.LOCAL.value:
            lines = CodeWriter.push_from_T("LCL", index_of_segment)
            return lines

        # push from argument:
        elif segment_type == Segments.ARGUMENT.value:
            lines = CodeWriter.push_from_T("ARG", index_of_segment)
            return lines

        # push from this:
        elif segment_type == Segments.THIS.value:
            lines = CodeWriter.push_from_T("THIS", index_of_segment)
            return lines

        # push from that:
        elif segment_type == Segments.THAT.value:
            lines = CodeWriter.push_from_T("THAT", index_of_segment)
            return lines

        # push from static
        elif segment_type == Segments.STATIC.value:
            lines = CodeWriter.push_from_static(index_of_segment,
                                                file_name)
            return lines

        #  push from pointer:
        elif segment_type == Segments.POINTER.value:
            lines = CodeWriter.push_from_pointer(index_of_segment)
            return lines

        # push from temp:
        elif segment_type == Segments.TEMP.value:
            index = int(index_of_segment)
            index = index + 5
            index_of_segment = str(index)
            lines = CodeWriter.push_from_temp(index_of_segment)
            return lines

        # push from some other segment
        lines = ["@" + index_of_segment,
                 "D=A",
                 "@" + segment_type,
                 "D=A+D",
                 "@SP",
                 "A=M",
                 "M=D",
                 "@SP",
                 "M=M+1"]
        return lines

    # ------- pop methods ---------

    @staticmethod
    def pop_to_static(index: str, function_name: str):
        """
        method to pop from stack to static
        :param function_name: function name where we pop from
        :param index:index we pop
        :return:
        """
        lines = ["@SP",
                 "M=M-1",
                 "A=M",
                 "D=M",
                 "@" + function_name + "." + index,
                 "M=D"]
        return lines

    @staticmethod
    def pop_to_pointer(segment: str):
        """
        method to pop from stack to pointer
        :param segment: segment this/that to pop to
        :return: array asm lines
        """
        lines = ["@SP",
                 "M=M-1",
                 "A=M",
                 "D=M",
                 "@" + segment,
                 "M=D"]
        return lines

    @staticmethod
    def pop_to_temp(index: str):
        """
        method to pop from stack to pointer
        :param index: index of temp to pop to from stack
        :return: array asm lines
        """
        lines = ["@SP",
                 "M=M-1",
                 "A=M",
                 "D=M",
                 "@R" + index,
                 "M=D"]
        return lines

    @staticmethod
    def pop_to_T(reg: str, index: str):
        """
        method to pop from this or that.
        :param index: [reg value]+index  =  value we pop into
        :param reg: register name
        :return: array asm lines
        """
        if reg == Segments.THAT.value:
            lines = ["@THAT"]
        elif reg == Segments.THIS.value:
            lines = ["@THIS"]
        elif reg == Segments.LOCAL.value:
            lines = ["@LCL"]
        else:
            lines = ["@ARG"]

        extend_lines = ["D=M",
                        "@" + index,
                        "D=D+A",
                        "@R13",
                        "M=D",
                        "@SP",
                        "M=M-1",
                        "A=M",
                        "D=M",
                        "@R13",
                        "A=M",
                        "M=D"]
        lines.extend(extend_lines)
        return lines

    @staticmethod
    def pop_line(file_name: str, line: str):
        """
        method to convert a pop line into an asm code
        :param file_name: file we are in, to name static variable
        :param line: the line to convert from vm to asm
        :return: array of asm code lines
        """
        without_pop = (line.split("pop")[1]).strip()
        segment_type = CodeWriter.get_segment_type(without_pop)
        index_of_segment = (line.split(segment_type.value)[1]).strip()

        #  POINTER POP
        if segment_type.value == Segments.POINTER.value:
            if index_of_segment == "0":
                return CodeWriter.pop_to_pointer("THIS")
            else:
                return CodeWriter.pop_to_pointer("THAT")

        # TEMP POP
        elif segment_type.value == Segments.TEMP.value:
            index_in_int = int(index_of_segment) + 5
            index_of_segment = str(index_in_int)
            return CodeWriter.pop_to_temp(index_of_segment)

        #  THIS / THAT / LOCAL / ARGUMENT POP
        elif (segment_type.value == Segments.THAT.value) | \
                (segment_type.value == Segments.THIS.value) | (
                segment_type.value == Segments.LOCAL.value) | (
                segment_type.value == Segments.ARGUMENT.value):
            return CodeWriter.pop_to_T(segment_type.value, index_of_segment)

        # STATIC POP
        elif segment_type.value == Segments.STATIC.value:
            lines = CodeWriter.pop_to_static(index_of_segment, file_name)
            return lines

        else:
            line_00 = "@" + index_of_segment
            line_01 = "D=A"

            # we put into @addr some value a.
            line_1 = "@addr"
            line_2 = "M=D"

            # we look at the segment first address, and put it into D
            line_3 = "@" + segment_type.value
            line_4 = "D=M"

            # then we add to addr the address of segment
            # so addr = address of segment[a]
            line_5 = line_1  # @addr
            line_6 = "M=D+M"
            line_7 = line_4  # @D=M

            # not we point @addr to segment[a],
            line_8 = line_1  # @addr
            line_9 = "A=D"

            # not we put into the D the value in the stack top.
            line_10 = "@SP"
            line_11 = line_4

            # we loot at addr, which points at segment[a]
            # and put into its value (M) the stack top (D)
            line_12 = line_1  # @addr
            line_13 = "M=D"

            # not we lower down the stack, because we poped a value
            line_14 = line_10  # "@SP"
            line_15 = "A=A-1"

            return [line_00, line_01, line_1, line_2, line_3, line_4, line_5,
                    line_6, line_7, line_8,
                    line_9, line_10, line_11, line_12, line_13,
                    line_14, line_15]

    # ------- project 8 methods ---------

    @staticmethod
    def label_line(function_name: str, line: str):
        """
        method to convert a label line into an asm code
        :param function_name: function name under we are currently in
        :param line: the line to convert from vm to asm
        :return: array of asm code lines
        """
        # like said in Parser -  # ( functionName $ labelName )
        label_name = (line.split("label")[1]).strip()
        lines = ["(" + function_name + "$" + label_name + ")"]
        return lines

    @staticmethod
    def goto_line(function_name: str, line: str):
        """
        method to convert a goto line into an asm code
        :param line: the line to convert from vm to asm
        :param function_name: function where the label is located, the same
        function the goto line is in
        :return: array of asm code lines
        """

        without_goto = (line.split("goto")[1]).strip()
        label_name = without_goto
        # ( functionName $ labelName )
        # jump because it is a goto, we jump anyways.
        lines = ["@" + function_name + "$" + label_name,
                 "0;JMP"]
        return lines

    @staticmethod
    def if_line(function_name: str, line: str):
        """
        method to convert an if line into an asm code
        :param line: the line to convert from vm to asm
        :param function_name: function_name of where label is in
        :return: array of asm code lines
        """
        without_goto = (line.split("if-goto")[1]).strip()  # Eynam 27/11
        label_name = without_goto
        # ( functionName $ labelName )
        # we check what is last up the stack
        # if it is not zero, means NOT EQUAL ZERO then we jump,
        # which is D;JNE.
        lines = ["@SP",
                 "M=M-1",
                 "A=M",
                 "D=M",
                 "@" + function_name + "$" + label_name,
                 "D;JNE"]
        return lines

    @staticmethod
    def function_line(line: str):
        """
        method to convert a function declaration line into an asm code
        :param line: the line to convert from vm to asm
        :return: array of asm code lines
        """
        function_name, k_args = CodeWriter.parse_call_function_line(line,
                                                                    "function")

        lines = ["(" + function_name + ")"]

        push_0 = ["@0",
                  "D=A",
                  "@SP",
                  "A=M",
                  "M=D",
                  "@SP",
                  "M=M+1"]

        # push 0 k times
        # making space for k LOCALS for the function
        for i in range(int(k_args)):
            lines.extend(push_0)

        return lines

    @staticmethod
    def return_line():
        """
        method to convert a return line into an asm code
        :return: array of asm code lines
        """

        # Eynam 28/11 Hypothetically it works, but maybe it doesn't
        # can shorten this by about 5 lines (if it works ofc)
        lines = ["@LCL",
                 "D=M",
                 "@temp.FRAME",  # saving LCL in temp.FRAME
                 "M=D",
                 "@5",
                 "D=D-A",  # D = (FRAME-5)
                 "A=D",
                 "D=M",  # calculating *(FRAME-5)
                 "@temp.RET",
                 "M=D",  # saving *(FRAME-5) in temp.RET
                 "@SP",  # pop
                 "M=M-1",  # pop
                 "A=M",  # pop
                 "D=M",  # pop
                 "@ARG",  # *arg=pop()
                 "A=M",
                 "M=D",
                 "@ARG",
                 "D=M",
                 "@SP",
                 "M=D+1", #sp=arg+1
                 "@temp.FRAME",  # start of that,this,arg,local, starting to
                 # return to caller function state
                 "M=M-1",  # FRAME-1
                 "A=M",  # *(FRAME-1)
                 "D=M",
                 "@THAT",
                 "M=D",  # THAT = *(FRAME-1)
                 "@temp.FRAME",
                 "M=M-1",  # FRAME-1-1=FRAME-2
                 "A=M",  # *(FRAME-2)
                 "D=M",
                 "@THIS",
                 "M=D",  # THIS = *(FRAME-2)
                 "@temp.FRAME",
                 "M=M-1",  # FRAME-2-1=FRAME-3
                 "A=M",  # *(FRAME-3)
                 "D=M",
                 "@ARG",
                 "M=D",  # ARG = *(FRAME-3)
                 "@temp.FRAME",
                 "M=M-1",  # FRAME-3-1=FRAME-4
                 "A=M",  # *(FRAME-4)
                 "D=M",
                 "@LCL",
                 "M=D",  # LCL = *(FRAME-4)
                 "@temp.RET",
                 "A=M",  # getting return address which is inside,
                 # because temp.RET holds where the return address is kept.
                 "0;JMP"]  # jumping to RET value by the value in M.
        return lines

    @staticmethod
    def call_line(return_address: str, line: str):
        """
        method to convert a function call line into an asm code
        :param return_address: label which we go to
        :param line: the line to convert from vm to asm
        :return: array of asm code lines
        """
        function_name, n_args = CodeWriter.parse_call_function_line(line,
                                                                    "call")

        lines = list()
        # push return address
        push_return = CodeWriter.push_address(return_address)
        lines.extend(push_return)

        # go through CALL_DICTIONARY -> [LCL, ARG, THIS, THAT]
        for i in range(len(CALL_DICTIONARY)):
            # saving states of LCL, ARG, THIS, THAT
            lines.extend(CodeWriter.push_registers(CALL_DICTIONARY[i]))

        arg_insertion = ["// ARG=SP-n-5",
                         "@5",
                         "D=A",
                         "@" + n_args,
                         "D=A+D",  # n+5
                         "@SP",
                         "D=M-D",  # SP-(n+5)
                         "@ARG",
                         "M=D"]  # ARG = SP-n-5
        lcl_insertion = ["// LCL = SP",
                         "@SP",
                         "D=M",  # D = SP
                         "@LCL",
                         "M=D"]  # SP = D

        goto_function = ["@" + function_name,  # going to function
                         "0;JMP"]

        declaration_function = ["(" + return_address +
                                ")"]  # where we return to afterwards
        # arg block from above
        lines.extend(arg_insertion)
        # lcl block from above
        lines.extend(lcl_insertion)
        # goto function we are calling
        lines.extend(goto_function)

        # where we come back after function
        lines.extend(declaration_function)
        return lines

    # ------- Sys.init line ---------

    @staticmethod
    def write_init():
        """
        method to write the sys.init function 
        :return:
        """
        # Eynam 27/11
        lines = ["// sys.init start",
                 "@256",
                 "D=A",
                 "@SP",
                 "M=D"]
        sys_init = "Sys.init$ret.0"
        sys_init_call = CodeWriter.call_line(sys_init, "call Sys.init 0")
        sys_init_call.append("// sys.init end")
        lines.extend(sys_init_call)
        return lines

    # ------- project 8 helper methods ---------
    @staticmethod
    def push_address(segment: str):
        lines = ["@" + segment,
                 "D=A",
                 "@SP",
                 "A=M",
                 "M=D",
                 "@SP",
                 "M=M+1"]
        return lines

    @staticmethod
    def push_registers(segment: str):
        lines = ["@" + segment,
                 "D=M",
                 "@SP",
                 "A=M",
                 "M=D",
                 "@SP",
                 "M=M+1"]
        return lines

    @staticmethod
    def parse_call_function_line(line: str, split_str: str):
        """
        method to parse the "split_str f n" line into f(function name) and n
        :param split_str: str to split by
        :param line: the line given
        :return: f name, and n_args int
        """
        without_call = (line.split(split_str)[1]).strip()
        split_array = without_call.split()
        function_name = split_array[0]
        n_args = split_array[1]
        return function_name, n_args

    DICTIONARY = {Arithmetics.ADD.value: handle_add.__get__(object),
                  Arithmetics.SUB.value: handle_sub.__get__(object),
                  Arithmetics.NEG.value: handle_neg.__get__(object),
                  Arithmetics.EQ.value: handle_eq.__get__(object),
                  Arithmetics.GT.value: handle_gt.__get__(object),
                  Arithmetics.LT.value: handle_lt.__get__(object),
                  Arithmetics.AND.value: handle_and.__get__(object),
                  Arithmetics.OR.value: handle_or.__get__(object),
                  Arithmetics.NOT.value: handle_not.__get__(object)}
