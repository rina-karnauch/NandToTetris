"""
removes all comments and white space from the input
stream and breaks it into jack-language tokens, as specified
by the jack grammar.
-------------------------------------------------------
     ** unit 9.8 shows how to tokenize it all **
-------------------------------------------------------
"""
import re
from lxml import etree
from typing import Tuple

KEYWORD_TYPE = "keyword"
SYMBOL_TYPE = "symbol"
INT_TYPE = "integerConstant"
STRING_TYPE = "stringConstant"
IDENTIFIER_TYPE = "identifier"

UNARY = {"-", "~"}


def array_regex_helper(words):
    """
    method to handle -(var)
    :param words: array words
    :return: new array of words
    """
    new_words = list()
    for word in words:
        if (word[0] in UNARY) and (len(word) > 1):
            new_words.append(word[0])
            new_words.append(word[1:])
        elif (word[0] in UNARY) and (len(word) == 1):
            new_words.append(word)
        else:
            new_words.append(word)
    return new_words


class JackTokenizer:

    def __init__(self, input_file: str):
        """
        opens the input file/stream
        and gets ready to tokenize it
        ** input_file is a ONE jack file to tokenize. **
        :param input_file: input file we are given with
        """
        # for our usage:
        self.keyword_list = {'class', 'constructor', 'function',
                             'method', 'field', 'static', 'var', 'int',
                             'char', 'boolean', 'void', 'true', 'false',
                             'null', 'this', 'let', 'do', 'if', 'else',
                             'while',
                             'return'}
        self.symbol_list = {'{', '}', '(', ')', '[', ']', '.', ',', ';',
                            '+', '-', '*', '/', '&', '|', '<', '>', '=', '~'}

        self.int_range = range(0, 32767)

        # for our tokenization usage
        self.tokens = None
        self.current_word = None
        self.current_type = None
        self.current_index = -1
        self.length = -1

        # tokenization
        self.input_file_name = input_file
        self.input_file = open(input_file, 'r')

        # for regexes
        self.joined_keyword_list = "$"
        self.joined_keyword_list = self.joined_keyword_list + '|$'.join(
            self.keyword_list)
        self.joined_symbol_list = "".join(self.symbol_list)

        # regexes

        self.split_by_string = re.compile(r'"[^"\n]*"')
        self.split_by_keyword = re.compile(self.joined_keyword_list)
        self.split_by_int = re.compile(r"\d+")
        self.split_by_identifier = re.compile(r"^[a-zA-Z_][a-zA-Z0-9_]+")
        # escape is for preventing regex to confuse symbols it knows
        # with symbols in text
        self.split_by_symbol = re.compile(
            '[' + re.escape(self.joined_symbol_list) + ']')

        # all combined

        self.regex_list = "|".join([r'"[^"\n]*"',
                                    self.joined_keyword_list,
                                    r"\d+",
                                    r"[a-zA-Z_][a-zA-Z0-9_]*",
                                    '[' + re.escape(
                                        self.joined_symbol_list) + ']'])
        self.all_regexes = re.compile(self.regex_list)

        # list of all all all words!
        self.file_words = self.input_file.readlines()
        self.remove_comments_and_strip_lines()
        self.xmlT_output = None

    def remove_comments_and_strip_lines(self) -> None:
        """
        method to remove comments out of lines and strip lines
        :return: none
        """
        new_words = list()
        length = len(self.file_words)
        i = 0
        while i < length:

            line = self.file_words[i]
            line = line.lstrip()
            line = line.rstrip()

            if line == "":
                i = i + 1
                continue

            if line.startswith("/**") | line.startswith("/*"):
                next_line = self.file_words[i].rstrip()
                while not next_line.endswith("*/"):
                    i = i + 1
                    next_line = self.file_words[i].rstrip()

            elif not (line.startswith("//") | line.startswith("*")):
                line = JackTokenizer.clean_line(line)
                line = line.rstrip()
                line = line.lstrip()
                words = self.all_regexes.findall(line)
                words = array_regex_helper(words)
                new_words.extend(words)

            i = i + 1
        self.file_words = new_words

    @staticmethod
    def clean_line(line: str) -> str:
        new_line = re.sub("(?s)/\\*.*\\*/", "", line)
        line = new_line
        if "//" in line:
            if '"' in line:
                first_q_index = line.index('"')
                second_q_index = line.index('"', first_q_index + 1)
                comment_index = line.index("//")
                if (comment_index < first_q_index) | (comment_index > \
                        second_q_index):
                    line = line.split("//")
                    line = line[0]
            else:
                line = line.split("//")
                line = line[0]
        return line

    @staticmethod
    def add_line(line: str) -> bool:
        """
        method to check if we should pass line
        :param line: to check
        :return: true if add line false otherwise
        """
        if line.isspace():
            return False
        line = line.rstrip()
        line = line.lstrip()
        if line.startswith("/**"):
            return False
        elif line.endswith("*/"):
            return False
        elif line.startswith("*"):
            return False
        elif line.startswith("//"):
            return False
        elif line.endswith("*/"):
            return False
        elif line == "":
            return False
        return True

    def tokenize(self) -> None:
        """
        creates a list of tokens for the xml file, word by word
        """
        self.tokens = list()
        for word in self.file_words:
            self.current_word = word
            self.tokens.append(self.read_token())
        self.length = len(self.tokens)
        self.current_index = -1
        # self.write_xml_file()

    def get_tokens(self):
        """
        method to get tokenized array
        :return: array of tuples of (token type, token string)
        """
        return self.tokens

    def read_token(self) -> Tuple[str, str]:
        """
        method to read current word into a token
        :return: tuple of (type, token_content)
        """
        token_type = self.token_type()
        token_content = None
        if token_type == KEYWORD_TYPE:
            token_content = self.keyword()
        elif token_type == IDENTIFIER_TYPE:
            token_content = self.identifier()
        elif token_type == SYMBOL_TYPE:
            token_content = self.symbol()
        elif token_type == STRING_TYPE:
            token_content = self.string_value()
        elif token_type == INT_TYPE:
            token_content = self.int_value()
        return token_type, token_content

    def has_more_tokens(self) -> bool:
        """
        checks if we have more token in input
        :return: true for more tokens, false otherwise
        """
        return self.current_index < self.length - 1

    def advance(self):
        """
        gets the next token from the input
        and makes it the current token
        ** CALLED ONLY IF has_more_tokens
        :return: none
        """
        self.current_index = self.current_index + 1
        if self.has_more_tokens():
            self.current_word = self.tokens[self.current_index][1]
            self.current_type = self.tokens[self.current_index][0]

    def get_current_token(self):
        """
        method to get current token we process
        :return:
        """
        return self.tokens[self.current_index]

    def peek_at_next_token(self):
        """
        method to peek at next token without forwarding
        :return: tuple of type and string
        """
        if self.current_index + 1 == self.length:
            return None
        return self.tokens[self.current_index + 1]

    def token_type(self):
        """
        returns the type of the current token
        :return: type of token out of
        {KEYWORD, SYMBOL, IDENTIFIER,
        INT_CONST, STRING_CONST}
        """
        if self.current_word in self.keyword_list:
            return KEYWORD_TYPE
        elif self.current_word in self.symbol_list:
            return SYMBOL_TYPE
        elif self.regex_check_for_integer():
            integer = int(self.current_word)
            if integer in self.int_range:
                # in range of 0 to 32767
                return INT_TYPE
            # ************** handle otherwise ************** #
        elif self.regex_check_for_string():
            return STRING_TYPE
        else:
            # identifier for sure
            return IDENTIFIER_TYPE

    def regex_check_for_string(self):
        """
        method to check if current word matches a string regex
        :return: true or false
        """
        regex = self.split_by_string
        return regex.match(self.current_word)

    def regex_check_for_integer(self):
        """
        method to check if current word matches an integer regex
        :return: true or false
        """
        regex = self.split_by_int
        return regex.match(self.current_word)

    def write_xml_file(self) -> None:
        """
        method to write xml lines in file
        :return: none
        """

        tokens_root = etree.Element("tokens")
        for token_pair in self.tokens:
            token_type = token_pair[0]
            token_content = " " + token_pair[1] + " "
            etree.SubElement(tokens_root, token_type).text = token_content
        xml_file_name = self.input_file_name.replace(".jack", "") + "T2"
        xml_file_name = xml_file_name + ".xml"
        self.xmlT_output = open(xml_file_name, 'wb')

        tree = etree.ElementTree(tokens_root)
        etree.indent(tokens_root, "")
        tree.write(self.xmlT_output, pretty_print=True)
        self.xmlT_output.close()

    def keyword(self) -> str:
        """
        return the keyword which is the current token.
        ** CALLED ONLY IF token_type = KEYWORD
        :return:  type of key word out of
        {CLASS, METHOD, FUNCTION, CONSTRUCTOR,
        INT, BOOLEAN, CHAR, VOID, VAR,
        STATIC, FIELD, LET, DO, IF, ELSE,
        WHILE, RETURN, TRUE, FALSE, NULL, THIS}
        { 'class' | 'constructor' | 'function' |
        'method' | 'field' | 'static' | 'var' | 'int' |
        'char' | 'boolean' | 'void' | 'true' | 'false' |
        'null' | 'this' | 'let' | 'do' | 'if' | 'else' | 'while' | 'return'}
        """
        return self.current_word

    def symbol(self) -> str:
        """
        return the character which is the current token
        ** CALLED ONLY IF token_type = SYMBOL
        :return: character of
        {'{' | '}' | '(' | ')' | '[' | ']' | '.' | ','
        | ';' | '+' | '-' | '*' | '/' | '&' | '|' | '<' | '>' | '=' | '~'}
        """
        current_symbol = self.current_word
        # if current_symbol in self.html_dictionary:
        #     #  replacements for some symbols
        #     #    '<': "&lt",
        #     #    '>': "&gt",
        #     #    '"': "&quot",
        #     #    "&": "&amp"
        #     return self.html_dictionary[current_symbol]
        return self.current_word

    def identifier(self) -> str:
        """
        returns the identifier which is the current token.
        ** CALLED ONLY IF token_type = IDENTIFIER
        :return: string of {}
        """
        return self.current_word

    def int_value(self) -> int:
        """
        returns the integer value which is the current token.
        ** CALLED ONLY IF token_type = INT_CONST
        :return: int from 0 to 32767(?)
        """
        return self.current_word

    def string_value(self) -> str:
        """
        returns the string value which is the current token.
        ** CALLED ONLY IF token_type = STRING_CONST
        :return: string
        """
        return self.current_word
