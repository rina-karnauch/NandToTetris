# rina.karnauch, came1337
# =============================================================================
# Rina Karnauch, ID 319132353, rina.karnauch@mail.huji.ac.il
# Eynam Wassertheil, ID 207557935, eynam.wassertheil@mail.huji.ac.il
# =============================================================================
from enum import Enum

CONSTANT_RANGE = 32767


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
                 "D;JGT",
                 "D=0",
                 "@INSERT" + counter,
                 "0;JMP",
                 "(DIFFSIGNS" + counter + ")",
                 "@SP",
                 "A=M",
                 "D=M",
                 "@SP",
                 "A=M-1",
                 "D=M-D",
                 "D=-D",
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
                 "@SP",
                 "A=M-1",
                 "D=M-D",
                 "D=-D",
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
    def push_from_static(index: str):
        """
        push from constant into stack
        :param index: index to push
        :return: asm lines
        """
        lines = ["@Foo." + index,
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
    def push_line(counter: str, line: str):
        """
        method to convert a push line into an asm code
        :param counter: counter of push
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
            lines = CodeWriter.push_from_static(index_of_segment)
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
    def pop_to_static(index: str):
        """
        method to pop from stack to static
        :param index:
        :return:
        """
        # Foo. -> file name.
        # segment of static is static to the current file name
        # therefore the statics are name according to filename.(index)
        # and index is the pop static (index)
        # therefore we pop into the static segment inside the file name in
        # place index, meaning (index)'th static variable of current
        # file name
        lines = ["@SP",
                 "M=M-1",
                 "A=M",
                 "D=M",
                 "@Foo." + index,
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
    def pop_line(counter: str, line: str):
        """
        method to convert a pop line into an asm code
        :param counter: counter for labels
        :param line: the line to convert from vm to asm
        :return: array of asm code lines
        """
        without_pop = (line.split("pop")[1]).strip()
        segment_type = CodeWriter.get_segment_type(without_pop)
        index_of_segment = (line.split(segment_type.value)[1]).strip()

        #  POINTER POP
        # pop pointer 0/1
        # is actually pop the value in the stack
        # into the THIS when (0) or THAT when (1)
        # meaning,  when we have pop pointer 0
        # we pop the stack value into THIS holder which is RAM[3]
        # otherwise if we have pop pointer 1 we pop the
        # stack value into THAT holder which is RAM[4]

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
            return CodeWriter.pop_to_static(index_of_segment)

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
    def label_line(line: str):
        """
        method to convert a label line into an asm code
        :param line: the line to convert from vm to asm
        :return: array of asm code lines
        """
        print(line)

    @staticmethod
    def goto_line(line: str):
        """
        method to convert a goto line into an asm code
        :param line: the line to convert from vm to asm
        :return: array of asm code lines
        """
        print(line)

    @staticmethod
    def if_line(line: str):
        """
        method to convert an if line into an asm code
        :param line: the line to convert from vm to asm
        :return: array of asm code lines
        """
        print(line)

    @staticmethod
    def function_line(line: str):
        """
        method to convert a function declaration line into an asm code
        :param line: the line to convert from vm to asm
        :return: array of asm code lines
        """
        print(line)

    @staticmethod
    def return_line(line: str):
        """
        method to convert a return line into an asm code
        :param line: the line to convert from vm to asm
        :return: array of asm code lines
        """
        print(line)

    @staticmethod
    def call_line(line: str):
        """
        method to convert a function call line into an asm code
        :param line: the line to convert from vm to asm
        :return: array of asm code lines
        """
        print(line)

    DICTIONARY = {Arithmetics.ADD.value: handle_add.__get__(object),
                  Arithmetics.SUB.value: handle_sub.__get__(object),
                  Arithmetics.NEG.value: handle_neg.__get__(object),
                  Arithmetics.EQ.value: handle_eq.__get__(object),
                  Arithmetics.GT.value: handle_gt.__get__(object),
                  Arithmetics.LT.value: handle_lt.__get__(object),
                  Arithmetics.AND.value: handle_and.__get__(object),
                  Arithmetics.OR.value: handle_or.__get__(object),
                  Arithmetics.NOT.value: handle_not.__get__(object)}
