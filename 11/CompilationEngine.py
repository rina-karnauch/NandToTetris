"""
gets input from a jack tokenizer and emits its
parsed structure into an output file/stream.
-------------------------------------------------------
    ** unit 10.5 shows how to compile with it **
    STEPS:
    1. do without expressions
    2. handle expressions
-------------------------------------------------------
"""
from lxml import etree
import JackTokenizer
from SymbolTable import SymbolTable
from VMWriter import VMWriter

CLASS_VAR_DEC = "classVarDec"
VAR_DEC = "varDec"
SUBROUTINE_DEC = "subroutineDec"
SUBROUTINE_BODY = "subroutineBody"
PARAM_LIST = "parameterList"
STATEMENTS = "statements"
EXPRESSION_LIST = "expressionList"
EXPRESSION = "expression"
TERM = "term"

# ----- identifier type, project 11, Wednesday -------- #
LOCAL = "local"
ARGUMENT = "argument"
STATIC = "static"
FIELD = "field"
SUBROUTINE = "subroutine"

USED = "used"
DEFINED = "defined"
# ----------------------------------------------------- #

COMMA = ","
DOT = "."
COMMA_DOT = ";"
END_OF_PARAM_LIST = ")"
START_OF_PARAM_LIST = "("
ARRAY_OPENER = "["
ARRAY_CLOSER = "]"
END_OF_CLASS = "}"

LET = "let"
IF = "if"
ELSE = "else"
WHILE = "while"
DO = "do"
RETURN = "return"
STATEMENT_STR = "Statement"
METHOD = "method"
CONSTRUCTOR = "constructor"
VOID = "void"

NAME = "name"
TYPE = "type"
KIND = "kind"
INDEX = "index"

ADD = "add"

ZERO_NUM = 0
ONE_NUM = 1
TWO_NUM = 2

LABEL = "L"

CONSTANT = "constant"
POINTER = "pointer"
THAT = "that"
THIS = "this"
TEMP = "temp"

TRUE = "true"
FALSE = "false"
NULL = "null"

ALLOCATION_METHOD = "Memory.alloc"
STRING_ALLOC_METHOD = "String.new"
STRING_APPENDING = "String.appendChar"

BINARY_OPERATORS = {"+", "-", "*", "/", "&", '"', "|", ">", "<", "="}

BINARY_DICT = {"+": "add", "-": "sub", "*": "call Math.multiply 2",
               "/": "call "
                    "Math.divide 2", "&": "and", "|": "or", ">": "gt",
               "<": "lt", "=": "eq", "!": "neg", "~": "not"}

UNARY_OPERATORS = {"-", "~"}
KEYWORD_CONSTS = {"true", "false", "null", "this"}


class CompilationEngine:

    def __init__(self, input_stream: str, jack_tokenizer: JackTokenizer):
        """
        creates a new compilation engine with the given
        input and output.
        :param input_stream: given input stream
        :param jack_tokenizer: given jack tokenizer
        """
        self.tokenizer = jack_tokenizer
        self.tokens = jack_tokenizer.get_tokens()
        self.file_name = input_stream.replace(".jack", "")
        self.output_file_name = input_stream.replace(".jack", ".xml")
        self.output_file = open(self.output_file_name, "wb")
        self.current_class_name = None
        self.root = None
        self.label_counter = 0
        self.tree = None

        # ----- identifier type, project 11, Wednesday -------- #
        self.identifier_counter = {LOCAL: 0,
                                   ARGUMENT: 0,
                                   STATIC: 0,
                                   FIELD: 0}
        # ----------------------------------------------------- #

        self.symbol_table = SymbolTable()
        self.VMWriter = None

    def compile(self) -> None:
        """
        method to compile jack file and close file afterwards
        :return: none
        """
        self.tokenizer.advance()
        self.compile_class()
        self.output_file.close()

    def compile_class(self) -> None:
        """
        compiles a class
        :return: None
        """

        # create VMWriter for current class
        self.VMWriter = VMWriter(self.file_name)

        # was class
        self.tokenizer.advance()
        # now name

        # current class name :
        self.current_class_name = self.tokenizer.get_current_token()[1]

        # was name
        self.tokenizer.advance()
        # now {

        # was {
        self.tokenizer.advance()
        # now class body

        while self.tokenizer.has_more_tokens():
            current_token = self.tokenizer.get_current_token()
            token_string = current_token[1]
            if CompilationEngine.is_class_field(token_string):
                self.compile_class_var_declaration()
            elif CompilationEngine.is_subroutine(token_string):
                self.compile_subroutine()

        # insert last  "}" of end of class
        current_token = self.tokenizer.get_current_token()[1]
        self.tokenizer.advance()

        # # ***** testing  ***** #
        # tree = etree.ElementTree(self.root)
        # # etree.indent(self.root, "")
        # tree.write(self.output_file, pretty_print=True)

    @staticmethod
    def is_subroutine(token: str) -> bool:
        """
        method to check if token is subroutine
        :param token: string of current token
        :return: true if subroutine declaration, false otherwise
        """
        return ((token == "constructor") or (token == "function") or (
                token == "method"))

    @staticmethod
    def is_var_declare(token: str) -> bool:
        return token == "var"

    @staticmethod
    def is_class_field(token: str) -> bool:
        """
        method to check if token is class field
        :param token: string of current token
        :return: true if class field declaration, false otherwise
        """
        return (token == "static") or (token == "field")

    @staticmethod
    def is_statement(token: str) -> bool:
        return (token == LET) or (token == IF) or (token == WHILE) or (
                token == DO) or (token == RETURN)

    def insert_next_token(self, root) -> None:
        """
        insert next token
        :return: none
        """
        current_token = self.tokenizer.get_current_token()
        token_type = current_token[0]
        token_string = current_token[1]

        if token_type == JackTokenizer.STRING_TYPE:
            token_string = token_string[1:-1]

        etree.SubElement(root, token_type).text = " " + token_string + " "
        self.tokenizer.advance()

    def compile_class_var_declaration(self) -> None:
        """
        compiles a variable declaration
        :return: None
        """

        # variable kind: field | static
        kind = self.tokenizer.get_current_token()[1]
        # field | static
        self.tokenizer.advance()

        # variable type
        type_var = self.tokenizer.get_current_token()[1]
        # int|char|boolean
        self.tokenizer.advance()

        # variable name
        name = self.tokenizer.get_current_token()[1]
        # varName
        self.tokenizer.advance()

        # adding to symbol table
        if kind == STATIC:
            # static variable
            self.identifier_counter[STATIC] += 1
        else:
            # class field
            self.identifier_counter[FIELD] += 1

        # adding to symbol table anyways
        self.symbol_table.define(name, type_var, kind)

        # run in a loop and print all names, with "," in between
        while self.tokenizer.current_word == COMMA:
            # ,
            self.tokenizer.advance()

            # need to add to symbol table as well
            # type is as before, and kind is as before
            # still needs to add to counter
            name = self.tokenizer.get_current_token()[1]

            # adding to symbol table
            if kind == STATIC:
                # static variable
                self.identifier_counter[STATIC] += 1
            else:
                # class field
                self.identifier_counter[FIELD] += 1

            # adding to symbol table anyways
            self.symbol_table.define(name, type_var, kind)

            # varName
            self.tokenizer.advance()

        # end of declaration
        # ;
        current_token = self.tokenizer.get_current_token()[1]
        self.tokenizer.advance()

    def compile_subroutine(self) -> None:
        """
        compiles a complete method
        function or constructor
        :return: None
        """

        # restart as a new subroutine
        self.symbol_table.start_subroutine()

        # constructor | function | method
        subroutine_type = self.tokenizer.get_current_token()[1]

        # add this if it is a method
        if subroutine_type == METHOD:
            name = THIS
            var_type = self.current_class_name
            kind = ARGUMENT
            self.symbol_table.define(name, var_type, kind)

        # was function type
        self.tokenizer.advance()
        # now return type

        # was return type
        self.tokenizer.advance()
        # now subroutine name
        subroutine_name = self.tokenizer.get_current_token()[1]

        subroutine_name = self.current_class_name + DOT + subroutine_name

        # was name
        self.tokenizer.advance()
        # now (

        # parameter list compilation
        # and inserting it into the subtree
        self.compile_parameter_list()

        # was )
        self.tokenizer.advance()
        # now {

        # subroutine body
        self.compile_subroutine_body(subroutine_name, subroutine_type)

        # was }
        self.tokenizer.advance()
        # now token
        return

    def compile_subroutine_body(self, subroutine_name: str,
                                subroutine_type: str):
        """
        method to compile subroutine body
        :return: None
        """

        n_locals = self.symbol_table.variable_counter[FIELD]

        # {
        current_token = self.tokenizer.get_current_token()[1]

        # vars inside
        var_count = 0

        # was {
        self.tokenizer.advance()
        current_token = self.tokenizer.get_current_token()[1]
        # now subroutine body

        # read all variable declares
        while CompilationEngine.is_var_declare(current_token):
            # adding var declare subtree
            # to subroutine body element tree
            var_count = var_count + self.compile_var_declaration()
            current_token = self.tokenizer.get_current_token()[1]

        # function declare line
        self.VMWriter.write_function(subroutine_name, var_count)

        # putting this
        if subroutine_type == CONSTRUCTOR:
            # allocate memory for object
            # subroutine is constructor

            # push const nLocals
            self.VMWriter.write_push(CONSTANT, n_locals)
            # call Memory.alloc 1
            self.VMWriter.write_call(ALLOCATION_METHOD, ONE_NUM)
            # (popping this): pop pointer 0
            self.VMWriter.write_pop(POINTER, ZERO_NUM)

        elif subroutine_type == METHOD:
            # push argument 0
            self.VMWriter.write_push(ARGUMENT, ZERO_NUM)
            # push pop pointer 0
            self.VMWriter.write_pop(POINTER, ZERO_NUM)

        # subroutine statements
        self.compile_statements()

        # }
        self.tokenizer.advance()

    def compile_var_declaration(self) -> int:
        """
        method to compile var declaration lines
        """

        var_count = 0

        # was var kind (var)
        kind = self.tokenizer.get_current_token()[1]
        self.tokenizer.advance()
        # now type

        # get type which is int|char|boolean|class
        type_var = self.tokenizer.get_current_token()[1]
        self.tokenizer.advance()
        # now name

        # get name which is int|char|boolean|class
        name = self.tokenizer.get_current_token()[1]
        self.tokenizer.advance()
        # now , or ;

        # adding to symbol table
        self.symbol_table.define(name, type_var, kind)

        var_count += 1

        # run in a loop and print all names, with "," in between
        while self.tokenizer.current_word == COMMA:
            # was ,
            var_count += 1
            self.tokenizer.advance()
            # now name

            # get name which for the int|char|boolean|class var
            name = self.tokenizer.get_current_token()[1]
            self.tokenizer.advance()
            # now , or ;

            # adding to symbol table
            self.symbol_table.define(name, type_var, kind)

        # end of declaration

        # was ;
        self.tokenizer.advance()
        # now next line
        return var_count

    def compile_parameter_list(self) -> int:
        """
        compiles a (CAN BE EMPTY) parameter list
        not including the enclosing "()"
        :return: var count of parameter list
        """
        var_count = 0

        # was (
        self.tokenizer.advance()
        current_token = self.tokenizer.get_current_token()[1]
        # now arguments or )

        # till we at the end of the param line -> ")"
        if current_token != END_OF_PARAM_LIST:

            var_count += 1
            kind = ARGUMENT

            # was var_type
            var_type = self.tokenizer.get_current_token()[1]
            self.tokenizer.advance()
            # now var name

            # was var_name
            name = self.tokenizer.get_current_token()[1]
            self.tokenizer.advance()
            # now , or )

            # possible_variable = self.get_variable_of_table(name)
            # if possible_variable is None:
            self.symbol_table.define(name, var_type, kind)
            # otherwise its inside

            current_token = self.tokenizer.get_current_token()[1]

            # go through param list
            while current_token == COMMA:
                var_count += 1

                # was ,
                self.tokenizer.advance()
                # now type

                # var_type
                var_type = self.tokenizer.get_current_token()[1]
                self.tokenizer.advance()
                # now var name

                # var_name
                name = self.tokenizer.get_current_token()[1]

                # possible_variable = self.get_variable_of_table(name)
                # if possible_variable is None:
                self.symbol_table.define(name, var_type, kind)
                # otherwise its inside

                self.tokenizer.advance()
                # now comma or )

                # check again current token
                current_token = self.tokenizer.get_current_token()[1]
        return var_count

    def compile_statements(self) -> None:
        """
        compiles a sequence of statements
        not including the enclosing {}
        :return: None
        """
        # statement
        current_token = self.tokenizer.get_current_token()[1]

        if current_token == END_OF_CLASS:
            # end of function we return
            return

        peek_at_next = current_token

        # peek statements as long as we have them
        # determine their type
        # add the statement block to the
        # over all statements blocks

        while CompilationEngine.is_statement(peek_at_next):
            # pretty much straight forward
            # we have some types of statements
            # and we need to find out which one
            # and send to the fitting compilation method
            if peek_at_next == LET:
                self.compile_let()
            elif peek_at_next == IF:
                self.compile_if()
            elif peek_at_next == WHILE:
                self.compile_while()
            elif peek_at_next == DO:
                self.compile_do()
            elif peek_at_next == RETURN:
                self.compile_return()
            # adding the statement was done inside
            # getting the token we are on
            peek_at_next = self.tokenizer.peek_at_next_token()[1]

    def compile_do(self) -> None:
        """
        compiles a do statement
        :return: None
        """

        # peeked on do
        # now advanced to do
        current_token = self.tokenizer.get_current_token()[1]
        if current_token != DO:
            self.tokenizer.advance()
            current_token = self.tokenizer.get_current_token()[1]

        # do
        self.tokenizer.advance()
        # what to do

        # --------------------------------------------- #
        # compilation of subroutine or some class routine
        # --------------------------------------------- #

        # subroutine_name
        # ------- or, for another class method  ---------
        # class_name  -> then .subroutine_name

        rout_or_class_name = self.tokenizer.get_current_token()[1]

        peek_at_token = self.tokenizer.peek_at_next_token()[1]

        if peek_at_token != START_OF_PARAM_LIST:
            self.tokenizer.advance()

        self.compile_call(rout_or_class_name)

        # now comes ;
        self.tokenizer.advance()

        # popping temp 0
        self.VMWriter.write_pop(TEMP, ZERO_NUM)

    def compile_let(self) -> None:
        """
        compiles a let statement
        --------------------
        let  "var_name" = "expression" ;
        --------------------
        :return: None
        """
        # peeked on let
        # now advanced to let
        current_token = self.tokenizer.get_current_token()[1]
        if current_token != LET:
            self.tokenizer.advance()
            current_token = self.tokenizer.get_current_token()[1]
        not_array_flag = True

        # should be varName, might be varName []
        # was let
        self.tokenizer.advance()
        var_name = self.tokenizer.get_current_token()[1]

        # now var name

        # was var name
        self.tokenizer.advance()
        current_token = self.tokenizer.get_current_token()[1]
        # now  =  or [

        if current_token == ARRAY_OPENER:
            not_array_flag = False
            self.calculate_memory_location(var_name)

        # were on =
        self.tokenizer.advance()
        # now on expression

        self.compile_expression()

        # after expression
        # comes;
        self.tokenizer.advance()

        if not_array_flag:
            # not array, we pop variable
            variable = self.get_variable_of_table(var_name)
            var_kind = variable[KIND]

            segment = SymbolTable.get_segment(var_kind)
            var_index = variable[INDEX]
            self.VMWriter.write_pop(segment, var_index)
        else:
            # array, we pop array element
            # pop temp 0
            self.VMWriter.write_pop(TEMP, ZERO_NUM)
            # pop pointer 1
            self.VMWriter.write_pop(POINTER, ONE_NUM)
            # push temp 0
            self.VMWriter.write_push(TEMP, ZERO_NUM)
            # pop that 0
            self.VMWriter.write_pop(THAT, ZERO_NUM)

    def calculate_memory_location(self, var_name):
        """
        method to calculate location of current var index
        :param var_name: name of variable
        :return:
        """
        # pushing name
        variable = self.get_variable_of_table(var_name)

        var_kind = variable[KIND]

        segment = SymbolTable.get_segment(var_kind)
        var_index = variable[INDEX]

        # after [
        self.tokenizer.advance()

        # expression inside array
        self.compile_expression()

        self.VMWriter.write_push(segment, var_index)
        # write add to add memory places
        self.VMWriter.write_arithmetic(ADD)

        # were on whats inside array
        self.tokenizer.advance()
        # now on ]

        # were on ]
        self.tokenizer.advance()
        # now on expression

    def compile_while(self):
        """
        compiles a while statement
        --------------------
        while  ( "expression" )
        { "statements }
        --------------------
        :return: None
        """

        # peeked on while
        # now advanced to let
        current_token = self.tokenizer.get_current_token()[1]
        if current_token != WHILE:
            self.tokenizer.advance()
            current_token = self.tokenizer.get_current_token()[1]

        # label L1
        while_label = self.label_generator()
        self.VMWriter.write_label(while_label)

        # while
        self.tokenizer.advance()
        # (
        self.tokenizer.advance()

        # expression of while
        self.compile_expression()

        # ~(cond)
        # negate condition
        negate = BINARY_DICT["~"]
        self.VMWriter.write_arithmetic(negate)
        #  --------------------  #

        # )
        self.tokenizer.advance()

        # if-goto L2
        after_while_label = self.label_generator()
        self.VMWriter.write_if(after_while_label)

        # {
        self.tokenizer.advance()

        # statement
        self.tokenizer.advance()

        self.compile_statements()

        # goto L1
        self.VMWriter.write_goto(while_label)

        # label L2
        self.VMWriter.write_label(after_while_label)

        # }
        self.tokenizer.advance()

    def compile_return(self) -> None:
        """
        compiles a return statement
        :return: None
        """
        # peeked on return
        # now advanced to return
        current_token = self.tokenizer.get_current_token()[1]
        if current_token != RETURN:
            self.tokenizer.advance()
            current_token = self.tokenizer.get_current_token()[1]

        value_to_return = self.tokenizer.peek_at_next_token()[1]

        if value_to_return == COMMA_DOT:
            # no value to return
            self.tokenizer.advance()
            self.VMWriter.write_push(CONSTANT, ZERO_NUM)
            self.VMWriter.write_return()
            return

        # evaluate return value
        self.tokenizer.advance()
        self.compile_expression()
        self.VMWriter.write_return()

        # ;
        self.tokenizer.advance()

    def compile_if(self):
        """
        compiles an if statement
        possibly with a trailing else clause
        --------------------
        if  ( "expression" )
        { "statements }
        - might be
        else {
        }
        --------------------
        :return: None
        """

        # peeked on if
        # now advanced to if
        current_token = self.tokenizer.get_current_token()[1]
        if current_token != IF:
            self.tokenizer.advance()
            current_token = self.tokenizer.get_current_token()[1]

        L1 = self.label_generator()
        L2 = self.label_generator()

        # was if now (
        self.tokenizer.advance()

        # cond
        # build if expression
        self.compile_expression()

        # ~(cond)
        # negate condition
        negate = BINARY_DICT["~"]
        self.VMWriter.write_arithmetic(negate)
        #  --------------------  #

        # )
        self.tokenizer.advance()

        # if-goto L1
        self.VMWriter.write_if(L1)
        #  --------------------  #

        # {
        self.tokenizer.advance()

        # insert whats inside if() { lalla }

        # VM code for s1
        self.compile_statements()
        #  --------------------  #

        # goto L2
        self.VMWriter.write_goto(L2)
        #  --------------------  #

        # }
        self.tokenizer.advance()

        # now we might have else:
        current_token = self.tokenizer.get_current_token()[1]
        current_peek = self.tokenizer.peek_at_next_token()[1]

        # label L1
        self.VMWriter.write_label(L1)
        #  --------------------  #

        # statements 2 is else :
        if (current_peek == ELSE) | (current_token == ELSE):
            if current_peek == ELSE:
                self.tokenizer.advance()
            # now else
            self.tokenizer.advance()
            # {
            self.tokenizer.advance()

            self.compile_statements()

            # }
            self.tokenizer.advance()

        # label L2
        self.VMWriter.write_label(L2)
        #  --------------------  #

    def compile_expression(self) -> None:
        """
        compiles an expression
        --------------------
        term (optional term)?
        term: var_name or constant
              - var_name: string with no digit
              - constant: decimal number
        --------------------
        :return: tree of an expression
        """

        # first term
        self.compile_term()

        peek_at_token = self.tokenizer.peek_at_next_token()[1]

        while peek_at_token in BINARY_OPERATORS:
            # binary op
            self.tokenizer.advance()
            operation = self.tokenizer.get_current_token()[1]

            # expression
            self.tokenizer.advance()

            # compile term
            self.compile_term()

            arithmetic_command = BINARY_DICT[peek_at_token]
            self.VMWriter.write_arithmetic(arithmetic_command)

            # renew again
            peek_at_token = self.tokenizer.peek_at_next_token()[1]

    def compile_term(self) -> None:
        """
        compiles a term.
        if the current token is an identifier  we distinguish between
        - a variable: .
        - an array entry: [
        - subroutine call: (
        :return: None
        """

        # get current token we insert
        current_token = self.tokenizer.get_current_token()
        token_type = current_token[0]
        token_string = current_token[1]

        # integerConstant
        if token_type == JackTokenizer.INT_TYPE:
            self.VMWriter.write_push(CONSTANT, token_string)

        # stringConstant
        elif token_type == JackTokenizer.STRING_TYPE:
            # construction of string inside
            self.construct_string(token_string)

        # keywordConstant
        elif token_type == JackTokenizer.KEYWORD_TYPE:
            if token_string == TRUE:
                self.VMWriter.write_push(CONSTANT, ZERO_NUM)
                neg_op = BINARY_DICT["~"]
                self.VMWriter.write_arithmetic(neg_op)
            if token_string == FALSE:
                self.VMWriter.write_push(CONSTANT, ZERO_NUM)
            elif token_string == THIS:
                self.VMWriter.write_push(POINTER, ZERO_NUM)
            elif token_string == NULL:
                self.VMWriter.write_push(CONSTANT, ZERO_NUM)

        # unaryOperator {- , ~}
        elif token_string in UNARY_OPERATORS:

            # operator to print after expression

            # we can not sub anything, we negate.
            if token_string == "-":
                token_string = "!"

            op = BINARY_DICT[token_string]

            self.tokenizer.advance()

            # create a term of the inside of the operator
            self.compile_term()
            # neg if -
            # not if ~
            self.VMWriter.write_arithmetic(op)
            # advance to next term

        # anyways we have a varNam or, varName[] or, subroutineCall () or ()

        # ( -> some expression -> )
        elif token_string == START_OF_PARAM_LIST:
            # (
            self.tokenizer.advance()
            # insert expression
            self.compile_expression()
            # )
            # advance to next term
            self.tokenizer.advance()

        else:
            # was some identifier
            possibly_parent = self.tokenizer.peek_at_next_token()[1]
            # now . or [

            # pretty much straight forward:
            # 1. array opener []
            # 2. expression opener () # function call
            # 3. className. -> and then # 2. call of subroutineName()
            # 4. simple varName
            if possibly_parent == ARRAY_OPENER:
                self.tokenizer.advance()
                self.array_variable(token_string)
            elif possibly_parent == START_OF_PARAM_LIST:
                # subroutine call immediately
                # (
                # lets compile it as a call.
                self.compile_call(token_string)
            elif possibly_parent == DOT:
                # .
                self.tokenizer.advance()
                # we have a possible className in token_string
                # now we will have a subroutine name and call
                self.compile_call(token_string)
            else:
                self.simple_variable(token_string)

    def simple_variable(self, var_name) -> None:
        """
        method to push simple variable
        :param var_name: var name we push
        :return: None
        """

        variable = self.get_variable_of_table(var_name)

        var_kind = variable[KIND]
        segment = SymbolTable.get_segment(var_kind)
        var_index = variable[INDEX]
        self.VMWriter.write_push(segment, var_index)

    def array_variable(self, var_name):

        variable = self.get_variable_of_table(var_name)

        var_kind = variable[KIND]
        var_index = variable[INDEX]
        segment = SymbolTable.get_segment(var_kind)

        # [
        self.tokenizer.advance()

        # expression inside []
        self.compile_expression()

        # push start of array
        self.VMWriter.write_push(segment, var_index)

        # handling writing to an array element
        # adding to base address, the expression
        self.VMWriter.write_arithmetic(ADD)
        # pop pointer 1
        self.VMWriter.write_pop(POINTER, ONE_NUM)
        # push that 0
        self.VMWriter.write_push(THAT, ZERO_NUM)

        # closing array
        # ]
        self.tokenizer.advance()

    def compile_expression_list(self) -> int:
        """
        compiles (might be empty list) a comma separated
        list of expression
        :return: amount of expressions
        """
        current_token = self.tokenizer.get_current_token()[1]
        # we are on (
        self.tokenizer.advance()
        # now we on ) or argument

        arguments_count = 0

        # we start unless we are already at ")"
        # just like with param list

        # or arg or )
        current_token = self.tokenizer.get_current_token()[1]

        if current_token != END_OF_PARAM_LIST:
            arguments_count += 1

            # compiling argument
            self.compile_expression()

            # close of expression
            self.tokenizer.advance()

            # renew current token
            current_token = self.tokenizer.get_current_token()[1]

            while current_token == COMMA:
                # was , -> now ) or argument
                self.tokenizer.advance()

                # now new argument
                arguments_count += 1
                # new expression tree
                self.compile_expression()
                # on term
                self.tokenizer.advance()
                # and go again, renew current token
                current_token = self.tokenizer.get_current_token()[1]

        return arguments_count

    def label_generator(self) -> str:
        """
        helper method
        method to generate new label
        :return: str of new label
        """
        label = LABEL + str(self.label_counter)
        self.label_counter += 1
        return label

    def construct_string(self, token_string):
        # need to call String.new
        token_string = token_string[1:-1]
        memory_to_alloc = len(token_string)
        self.VMWriter.write_push(CONSTANT, memory_to_alloc)
        # calling String.new 1, empty string of size (memory to alloc)
        self.VMWriter.write_call(STRING_ALLOC_METHOD, ONE_NUM)
        # need to add ascii value of chars:
        for char_of_string in token_string:
            ascii_value = ord(char_of_string)
            self.VMWriter.write_push(CONSTANT, ascii_value)
            self.VMWriter.write_call(STRING_APPENDING, TWO_NUM)

    def compile_call(self, rout_or_class_name) -> None:
        """
        method to compile call
        :param rout_or_class_name:  name of class or subroutine
        :return: none
        """
        variable = self.get_variable_of_table(rout_or_class_name)

        if variable is not None:
            rout_or_class_name = variable[TYPE]
            subroutine_type = variable[TYPE]
            var_index = variable[INDEX]
            var_kind = SymbolTable.get_segment(variable[KIND])
            self.VMWriter.write_push(var_kind, var_index)
        else:
            subroutine_type = None

        # . or subroutine name
        current_token = self.tokenizer.get_current_token()[1]
        if current_token == DOT:
            # it is a call for a className.subroutineName

            # was .
            self.tokenizer.advance()
            # now subroutine name

            # subroutine_name
            subroutine_name = self.tokenizer.get_current_token()[1]

            # Class.Subroutine
            subroutine_name = rout_or_class_name + DOT + subroutine_name
        else:
            # a subroutine name
            self.VMWriter.write_push(POINTER, ZERO_NUM)
            subroutine_name = self.current_class_name + DOT + rout_or_class_name
            subroutine_type = METHOD

        if (subroutine_type is None) | (subroutine_type == VOID):
            # other class of void
            arguments = 0
        else:
            # method or constructor
            arguments = 1

        # start of expression list
        # ------------------------
        # was subroutine name
        self.tokenizer.advance()
        # now (

        # compilation of expression list
        arguments = arguments + self.compile_expression_list()

        # -------------------- #
        # end of expression list
        # -------------------- #

        # call subroutine_name arguments
        self.VMWriter.write_call(subroutine_name, arguments)

    def get_variable_of_table(self, var_name):
        """
        method to get variable of one of tables
        :param var_name: var name to get
        :return: dict of variable
        """
        variable = None
        # if in both
        if (var_name in self.symbol_table.variable_table.keys()) & \
                (var_name in self.symbol_table.subroutine_table.keys()):
            variable = self.symbol_table.subroutine_table[var_name]
        elif var_name in self.symbol_table.variable_table.keys():
            variable = self.symbol_table.variable_table[var_name]
        elif var_name in self.symbol_table.subroutine_table.keys():
            variable = self.symbol_table.subroutine_table[var_name]
        return variable
