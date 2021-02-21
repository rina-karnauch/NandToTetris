# rina.karnauch, came1337
# =============================================================================
# Rina Karnauch, rina.karnauch@mail.huji.ac.il
# Eynam Wassertheil, eynam.wassertheil@mail.huji.ac.il
# =============================================================================
import glob
import os
import pathlib
import sys

import Parser

ARGUMENT_LINE_LEN = 2
FILE_NAME_INDEX = 1

from pathlib import Path


class VMTranslator:

    def __init__(self, file_name, list):
        """
        constructor of VMtranslator object
        :param file_name: file name of vm file
        """
        self.file_name = file_name
        self.parser = Parser.Parser(self.file_name)
        self.assembler_lines = list

    def transpiler(self):
        """
        method of transpiling from VM to ASM.
        :return: none
        """
        # name of file to print
        self.file_name = self.file_name.split("/")[-1].replace(".vm", "")
        self.assembler_lines.append(["//" + self.file_name])
        self.assembler_lines.extend(self.parser.parse())

    def output_into_file(self):
        """
        method to output VM lines we translated to our file, as ASM lines.
        :return:
        """
        name = self.file_name

        self.parser.file_name = name
        self.parser.init()

        lines = [self.parser.init_lines]
        lines.extend(self.assembler_lines)
        self.assembler_lines = lines

        with open(name, 'w') as out_file:
            for line in self.assembler_lines:
                if line is not None:
                    for sub_line in line:
                        if sub_line is not None:
                            out_file.write(sub_line + "\n")
        out_file.close()


def main():
    """
    main method to generate our process
    :return: none
    """
    if len(sys.argv) != ARGUMENT_LINE_LEN:
        print("Error: not given a file name")
        return
    vmTranslator = None
    file_name = sys.argv[FILE_NAME_INDEX]
    if file_name.endswith(".vm"):
        file_name = sys.argv[FILE_NAME_INDEX]
        curr_list = list()
        vmTranslator = VMTranslator(file_name, curr_list)
        vmTranslator.transpiler()
        vmTranslator.file_name = file_name.replace(".vm", ".asm")
        vmTranslator.output_into_file()
    else:
        abs_path = os.path.abspath(file_name)
        files = glob.glob(abs_path + "/*.vm")
        curr_list = list()
        for file in files:
            vmTranslator = VMTranslator(file, curr_list)
            vmTranslator.transpiler()
            curr_list = vmTranslator.assembler_lines

        new_path = pathlib.PurePath(abs_path)
        base_name = new_path.name
        new_name = abs_path + "/" + str(base_name) + ".asm"
        new_name = pathlib.PurePath(new_name)

        vmTranslator.file_name = new_name
        vmTranslator.output_into_file()


main()
