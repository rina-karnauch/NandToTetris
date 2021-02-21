##########################################
# name: Rina Karnauch, username: rina.karnauch
# name : Eynam Wassertheil, username: came1337
##########################################
import os
import sys

import Parser

ARGUMENT_LINE_LEN = 2
FILE_NAME_INDEX = 1


class Assembler:
    """
    a main class to create the file of the hack language translating
    create a new file and outputs the file
    """

    def __init__(self, file_name):
        """
        constructor of Assembler object
        :param file_name: file name of asm file
        """
        self.file_name = file_name
        self.parser = Parser.Parser(self.file_name)
        self.binary_lines = None

    def transpiler(self):
        """
        method of transpiling from ASM to OPCODE.
        :return: none
        """
        self.parser.line_sectioning()
        self.binary_lines = self.parser.parse()
        self.output_into_file()

    def output_into_file(self):
        """
        method to output binary lines into the file after transpiling
        :return:
        """
        name = self.file_name.replace(".asm", "")
        name = name + ".hack"
        with open(name, 'w') as out_file:
            for line in self.binary_lines:
                if line is not None:
                    out_file.write(line + "\n")
        out_file.close()


def main():
    """
    main method to generate our process
    :return: none
    """
    if len(sys.argv) != ARGUMENT_LINE_LEN:
        print("Error: not given a file name")
        return
    file_name = sys.argv[FILE_NAME_INDEX]
    if os.path.isdir(sys.argv[FILE_NAME_INDEX]):
        for file in os.listdir(file_name):
            if file.endswith(".asm"):
                file = file_name + "/" + file
                assembler = Assembler(file)
                assembler.transpiler()
    else:
        file_name = sys.argv[FILE_NAME_INDEX]
        assembler = Assembler(file_name)
        assembler.transpiler()


main()
