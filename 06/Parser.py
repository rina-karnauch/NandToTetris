##########################################
# name: Rina Karnauch, username: rina.karnauch
# name : Eynam Wassertheil, username: came1337
##########################################
from enum import Enum

from SymbolTable import SymbolTable

COMMENT = "//"
LABEL_START = "("
A_COMMAND_START = "@"
FIRST_ADDRESS = 16
SIXTEEN = 16
DESTINATIONS = {None: "000", "M": "001", "D": "010",
                "MD": "011", "A": "100", "AM": "101",
                "AD": "110",
                "AMD": "111"}

JUMPS = {None: "000", "JGT": "001", "JEQ": "010",
         "JGE": "011", "JLT": "100", "JNE": "101", "JLE": "110",
         "JMP": "111"}

COMP = {"0": "1110101010", "1": "1110111111", "-1": "1110111010",
        "D": "1110001100",
        "A": "1110110000", "M": "1111110000", "!D": "1110001101",
        "!A": "1110110001",
        "!M": "1111110001", "-D": "1110001111", "-A": "1110110011",
        "-M": "1111110011",
        "D+1": "1110011111", "A+1": "1110110111", "M+1": "1111110111", "D-1":
            "1110001110",
        "A-1": "1110110010", "M-1": "1111110010", "D+A": "1110000010", "D+M":
            "1111000010",
        "D-A": "1110010011", "D-M": "1111010011", "A-D": "1110000111", "M-D":
            "1111000111",
        "D&A": "1110000000", "D&M": "1111000000", "D|A": "1110010101", "D|M":
            "1111010101", "D<<": "1010110000", "D>>": "1010010000", "A<<":
            "1010100000",
        "A>>": "1010000000", "M<<": "1011100000",
        "M>>": "1011000000"}


class CommandType(Enum):
    """
    enum class of type of command
    """
    A_COMMAND = "A"
    C_COMMAND = "C"
    L_COMMAND = "L"


class Parser:
    """
    Encapsulates access to the input code.
    Reads an assembly language command, parses it, and provides convenient
    access to the commands components (fields and symbols).
    In addition, removes all white space and comments.
    """

    # init -> line sectioning -> read_labels -> read_A / read_C

    def __init__(self, file_name: str):
        """
        Opens the input file/stream and gets ready to parse it.
        :param file_name: file name to open
        """
        self.file = open(file_name)
        self.lines = self.file.readlines()
        self.clean_comments()

        self.current_line_index = 0
        self.current_line = self.lines[self.current_line_index]
        self.line_amount = len(self.lines)

        self.binary_lines = list()
        self.symbol_table = SymbolTable()
        self.labels = dict()

        self.next_address = FIRST_ADDRESS

    def clean_comments(self):
        """
        method to clean the comments from the code lines
        :return: none
        """
        new_lines = list()
        for line in self.lines:
            if ((not line.startswith("//")) & (not line.isspace()) &
                    (not line.startswith("/*") & (not line.startswith("*/")))):
                new_lines.append(line)
        self.lines = new_lines

    def parse(self):
        """
        method to parse out the file
        :return: none
        """
        self.read_labels()
        self.read_instructions()
        return self.binary_lines

    def strip_line(self):
        """
        method to strip \n or \t or spaces in line
        :return: none
        """
        self.current_line = self.current_line.strip()
        self.current_line = self.current_line.rstrip('\n')
        self.current_line = self.current_line.rstrip('\t')
        self.current_line = (self.current_line.split("//"))[0]
        self.current_line = self.current_line.replace(" ", "")

    def line_sectioning(self):
        """
        method to section lines of file by variable lines or label lines
        :return: none
        """
        # start sectioning
        while self.current_line is not None:
            # stripping from whitespaces and end line
            self.strip_line()
            self.lines[self.current_line_index] = self.current_line
            self.advance()

    def has_more_commands(self):
        """
        Are there more commands in the input?
        :return: true if has, false otherwise
        """
        if self.current_line_index + 1 < self.line_amount:
            return True
        return False

    def advance(self):
        """
        Reads the next command from
        the input and makes it the current command. Should be called only
        if hasMoreCommands() is true. Initially there is no current command.
        :return: none
        """
        if not self.has_more_commands():
            self.current_line = None
        while self.has_more_commands() & (
                self.current_line_index + 1 < self.line_amount):
            self.current_line_index = self.current_line_index + 1
            self.current_line = self.lines[self.current_line_index]
            # we shall not ignore:
            if not self.check_ignored_line():
                break

    def check_ignored_line(self):
        """
        check if a line should be ignored
        :return: true for ignored, false otherwise
        """
        if self.current_line.isspace():
            return True
        elif self.current_line.startswith(COMMENT):
            return True
        else:
            return False

    def get_address_for_symbol(self):
        """
        get next free address for a symbol in symbol table
        :return: int of address
        """
        address = self.next_address
        symbol_table = self.symbol_table

        while symbol_table.is_occupied(address):
            address = address + 1
        self.next_address = address + 1
        return address

    def read_labels(self):
        """
        read all labels inside the asm file
        and update symbol table accordingly
        :return: none
        """
        index = 0
        for line in self.lines:
            # if we are on a label:
            if Parser.line_command_type(line) == CommandType.L_COMMAND:
                # remove "(" and ")" from beginning and end.
                length_of_name = len(line)
                label_name = line[1:length_of_name - 1]
                # add to symbol table
                binary = Parser.decimal_to_binary(index)
                self.labels[label_name] = binary
                # label index is the number of line
                # the binary code of the label is its address
            else:
                index = index + 1

    @staticmethod
    def from_array_to_string(binary_string):
        """
        method to turn from an array of {0,1} into a string of {1,0}
        :param binary_string: binary array string
        :return: binary string
        """
        binary = ""
        binary = binary.join(binary_string)
        return binary

    def read_instructions(self):
        """
        method to read instructions of asm file
        :return: none
        """
        # instruction_lines: keys- line index, items- the line itself
        for instruction in self.lines:
            if Parser.line_command_type(instruction) == CommandType.A_COMMAND:
                binary = self.read_A_instruction(instruction)
                binary = Parser.from_array_to_string(binary)
                self.binary_lines.append(binary)
            elif Parser.line_command_type(instruction) == \
                    CommandType.C_COMMAND:
                binary = self.read_C_instruction(instruction)
                binary = Parser.from_array_to_string(binary)
                self.binary_lines.append(binary)

    def read_A_instruction(self, line: str):
        """
        read A instruction inside the asm file
        and update symbol table accordingly
        :return: binary code of line
        """
        if line[1].isdecimal():
            binary = Parser.decimal_to_binary(int(line[1:]))
        elif self.symbol_table.contains(line[1:]):
            binary = Parser.decimal_to_binary(self.symbol_table.get_address(
                line[1:]))
            binary = Parser.from_array_to_string(binary)
        elif line[1:] in self.labels.keys():
            binary = self.labels.get(line[1:])
        else:
            address = self.get_address_for_symbol()
            self.symbol_table.add_entry(line[1:], address)
            binary = Parser.decimal_to_binary(address)
        return Parser.from_array_to_string(binary)

    @staticmethod
    def read_C_instruction(line: str):
        """
        read C instruction inside the asm file
        and update symbol table accordingly
        :return: binary code of line
        """
        t1, t2, t3 = Parser.parse_C_command(line)

        # constructing string
        binary = ""

        # if (t2.isnumeric()) & (t1 == "A"):
        #    binary = (bin(int(t2)))[2:]
        #    rest = (16 - len(binary))*"0"
        #    binary = rest + binary
        #    return binary
        # else:

        # COMP, DESTINATIONS,JUMPS are dictionaries of fitting given commands
        binary = binary + COMP[t2]
        binary = binary + DESTINATIONS[t1]
        binary = binary + JUMPS[t3]
        return binary

    def read_L_instruction(self, label_name: str):
        """
        read L instruction inside the asm file
        :return: binary code of line
        """
        address = self.symbol_table.get_address(label_name)
        binary = Parser.decimal_to_binary(address)
        return Parser.from_array_to_string(binary)

    @staticmethod
    def decimal_to_binary(address):
        # because A instruction, first bit is 0->(15 bits we will display)
        binary = ['0'] * SIXTEEN
        # turns address into bin representation, for int.
        binary_address = (bin(address))[2:]
        binary_length = len(binary_address)
        from_index = SIXTEEN - binary_length
        # padding the string into binary.
        binary[from_index:SIXTEEN] = binary_address
        return binary

    def command_type(self):
        """
        Returns the type of the current command:
        - A_COMMAND for @Xxx where Xxx is either a symbol or a decimal number
        - C_COMMAND for dest=comp;jump
        - L_COMMAND (actually, pseudo- command) for (Xxx) where Xxx is a
        symbol.
        :return: enum of command type
        """
        if self.current_line.startswith(LABEL_START):
            return CommandType.L_COMMAND
        elif self.current_line.startswith(A_COMMAND_START):
            return CommandType.A_COMMAND
        else:
            # already deleted comments, so no need to check for that
            return CommandType.C_COMMAND

    @staticmethod
    def line_command_type(line: str):
        """
        Returns the type of the current command, out of the line itself.
        - A_COMMAND for @Xxx where Xxx is either a symbol or a decimal number
        - C_COMMAND for dest=comp;jump
        - L_COMMAND (actually, pseudo- command) for (Xxx) where Xxx is a
        symbol.
        :return: enum of command type
        """
        if line.startswith(A_COMMAND_START):
            return CommandType.A_COMMAND
        elif line.startswith(LABEL_START):
            return CommandType.L_COMMAND
        else:
            return CommandType.C_COMMAND

    @staticmethod
    def parse_C_command(line):
        """
        parsing a c command method, into 3 sections- dest, comp and jmp.
        :param line: given line to parse into a c command
        :return: a triplet of (dest, comp, jump)
        """
        # line looks like dest=comp;jmp

        # gives us [dest=comp],[jmp]
        # in an array
        # then we split second array to
        # [dest][comp]
        split_by_comma = line.split(';')
        split_by_equal = split_by_comma[0].split('=')
        if len(split_by_comma) == 1:
            # no jmp
            return split_by_equal[0], split_by_equal[1], None
        elif len(split_by_equal) == 1:
            # no dest
            return None, split_by_comma[0], split_by_comma[1]
        else:
            # dest and jmp
            return split_by_equal[0], split_by_equal[1], split_by_comma[1]