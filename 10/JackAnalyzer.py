"""
class of jack analyzer
"""
import glob
import os
import sys

from CompilationEngine import CompilationEngine
from JackTokenizer import JackTokenizer

"""
command line arguments amount
"""
ARGUMENT_LINE_LEN = 2
"""
index of file name in our command line
"""
FILE_NAME_INDEX = 1


class JackAnalyzer:

    def __init__(self, jack_input):
        """
        constructor of jack analyzer object
        :param jack_input: the input given to the jack analyzer,
               - a directory of jacks or a .jack itself.
        """
        self.jack_input = jack_input

    def handle_directory(self):
        """
        --------------------------------------------------
        WE WILL CREATE ONE .XML FILE FOR EVERY .JACK FILE
                  INSIDE THE directory_name dir
        --------------------------------------------------
        handling a directory of jack files
        :return: none
        """
        os.chdir(self.jack_input)
        jack_files_array = glob.glob("*.jack")
        for jack_file in jack_files_array:
            self.jack_input = jack_file
            self.handle_file()

    def handle_file(self):
        """
        --------------------------------------------------------------
        WE WILL CREATE ONE .XML FILE FOR OUR .JACK FILE NAME file_name
                          INSIDE WHERE file_name is
        --------------------------------------------------------------
        handling a file of jack
        :return: none
        """
        jack_tokenizer = JackTokenizer(self.jack_input)
        jack_tokenizer.tokenize()
        compilation_engine = CompilationEngine(self.jack_input, jack_tokenizer)
        compilation_engine.compile()


def main():
    """
    main method to run the jack analzyer with the given input from the terminal
    :return: none
    """
    if len(sys.argv) != ARGUMENT_LINE_LEN:
        print("Error: not given a file name")
        return
    jack_analyzer = None
    file_name = sys.argv[FILE_NAME_INDEX]
    if os.path.isdir(file_name):
        folder_name = file_name
        jack_analyzer = JackAnalyzer(folder_name)
        jack_analyzer.handle_directory()
    elif file_name.endswith('.jack'):
        # its a jack file name
        jack_analyzer = JackAnalyzer(file_name)
        jack_analyzer.handle_file()
    else:
        print("Error: not given a jack file or a folder")
        return


main()
