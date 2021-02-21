# rina.karnauch, came1337
# =============================================================================
# Rina Karnauch, rina.karnauch@mail.huji.ac.il
# Eynam Wassertheil, eynam.wassertheil@mail.huji.ac.il
# =============================================================================

from enum import Enum

from CodeWriter import CodeWriter

ARITHMETIC = ["add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"]
PUSH = "push"
POP = "pop"
GO_TO = "go"
LABEL = "label"
FUNCTION = "function"
IF = "if"
RETURN = "return"
CALL = "call"


class CommandType(Enum):
    """
    enum class of type of command
    """
    C_ARITHMETIC = "C_ARITHMETIC"
    C_PUSH = "C_PUSH"
    C_POP = "C_POP"
    C_LABEL = "C_LABEL"
    C_GOTO = "C_GOTO"
    C_IF = "C_IF"
    C_FUNCTION = "C_FUNCTION"
    C_RETURN = "C_RETURN"
    C_CALL = "C_CALL"

    # dictionary of handling methods
    LINE_TYPE_DICTIONARY = {C_ARITHMETIC: CodeWriter.arithmetic_line,
                            C_PUSH: CodeWriter.push_line,
                            C_POP: CodeWriter.pop_line,
                            C_LABEL: CodeWriter.label_line,
                            C_GOTO: CodeWriter.goto_line,
                            C_IF: CodeWriter.if_line,
                            C_FUNCTION: CodeWriter.function_line,
                            C_RETURN: CodeWriter.return_line,
                            C_CALL: CodeWriter.call_line}


class Parser:

    def __init__(self, file_name: str):
        self.file = open(file_name)
        self.lines = self.file.readlines()
        self.clean_comments()

        # will be list list lists
        # when assembler_lines[i][j] represents the line j in the assembler
        # code of line i in the vm code.
        # if line_i in vm is 5 lines in asm
        # assembler_lines[i][0] = // line_i (the line copied)
        # assembler_lines[i][1-5] = assembler code lines.
        self.assembler_lines = list()
        self.label_counter = 0

    @staticmethod
    def strip_line(line):
        """
        method to strip \n or \t or spaces in line
        :return: none
        """
        line = line.strip()
        line = line.rstrip('\n')
        line = line.rstrip('\t')
        line = (line.split("//"))[0]
        return line

    def clean_comments(self):
        """
        method to clean the comments from the code lines
        :return: none
        """
        new_lines = list()
        for line in self.lines:
            if ((not line.startswith("//")) & (not line.isspace()) &
                    (not line.startswith("/*") & (not line.startswith("*/")))):
                line = Parser.strip_line(line)
                new_lines.append(line)
        self.lines = new_lines

    def parse(self):
        """
        method to parse out the file
        :return: none
        """
        for line in self.lines:
            self.read_line(line)
        return self.assembler_lines

    @staticmethod
    def commandType(line):
        """
        method to return command type of a line
        :param line: line to determined type of
        :return: Command Type object
        """
        for start in ARITHMETIC:
            if line.startswith(start):
                return CommandType.C_ARITHMETIC
        if line.startswith(POP):
            return CommandType.C_POP
        elif line.startswith(PUSH):
            return CommandType.C_PUSH
        elif line.startswith(GO_TO):
            return CommandType.C_GOTO
        elif line.startswith(IF):
            return CommandType.C_IF
        elif line.startswith(CALL):
            return CommandType.C_CALL
        elif line.startswith(LABEL):
            return CommandType.C_LABEL
        elif line.startswith(RETURN):
            return CommandType.C_RETURN
        elif line.startswith(FUNCTION):
            return CommandType.C_FUNCTION
        else:
            return None

    def read_line(self, line):
        """
        method to read a line and create an ASM lines out of it
        :param line: the line in vm code to read
        :return: none
        """
        line_in_asm_array = list()
        documentation = "//" + line
        line_in_asm_array.append(documentation)
        command_type = Parser.commandType(line)

        # not supposed to happen:
        # if command_type is None:
        #    print("problem")

        dictionary = CommandType.LINE_TYPE_DICTIONARY.value
        handling_method = dictionary.get(command_type.value)
        translated_lines = handling_method(str(self.label_counter), line)
        self.label_counter = self.label_counter + 1
        line_in_asm_array.extend(translated_lines)
        self.assembler_lines.append(line_in_asm_array)
