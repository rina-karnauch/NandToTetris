"""
gets input from a jack tokenizer and emits its
parsed structure into an output file/stream.
-------------------------------------------------------
    ** unit 9.5 shows how to compile with it **
    STEPS:
    1. do without expressions
    2. handle expressions
-------------------------------------------------------
"""
from lxml import etree
import JackTokenizer

CLASS_VAR_DEC = "classVarDec"
VAR_DEC = "varDec"
SUBROUTINE_DEC = "subroutineDec"
SUBROUTINE_BODY = "subroutineBody"
PARAM_LIST = "parameterList"
STATEMENTS = "statements"
EXPRESSION_LIST = "expressionList"
EXPRESSION = "expression"
TERM = "term"

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

BINARY_OPERATORS = {"+", "-", "*", "/", "&", '"', "|", ">", "<", "="}
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
        self.output_file_name = input_stream.replace(".jack", ".xml")
        self.output_file = open(self.output_file_name, "wb")
        self.root = None
        self.tree = None

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
        # <class>
        self.root = etree.Element("class")
        # insert <keyword> class </keyword>
        self.insert_next_token(self.root)
        # insert <identifier> Square </identifier>
        self.insert_next_token(self.root)
        # insert <symbol> { </symbol>
        self.insert_next_token(self.root)

        while self.tokenizer.has_more_tokens():
            current_token = self.tokenizer.get_current_token()
            token_string = current_token[1]
            if CompilationEngine.is_class_field(token_string):
                self.compile_class_var_declaration()
            elif CompilationEngine.is_subroutine(token_string):
                self.compile_subroutine()

        # insert last  "}" of end of class
        self.insert_next_token(self.root)

        # ***** testing  ***** #
        tree = etree.ElementTree(self.root)
        # etree.indent(self.root, "")
        tree.write(self.output_file, pretty_print=True)

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
        # insert <classVarDec>
        class_var_dec_element = etree.Element(CLASS_VAR_DEC)

        # <keyword> field | static </keyword>
        self.insert_next_token(class_var_dec_element)
        # <keyword> int|char|boolean </keyword>
        self.insert_next_token(class_var_dec_element)
        # first variable name
        # <identifier> varName </identifier>
        self.insert_next_token(class_var_dec_element)

        # run in a loop and print all names, with "," in between
        while self.tokenizer.current_word == COMMA:
            # <symbol> , </symbol>
            self.insert_next_token(class_var_dec_element)
            # <identifier> varName </identifier>
            self.insert_next_token(class_var_dec_element)

        # end of declaration
        # <symbol> ; </symbol>
        self.insert_next_token(class_var_dec_element)

        self.root.append(class_var_dec_element)
        # etree.SubElement(self.root, class_var_dec_element)
        return

    def compile_subroutine(self) -> None:
        """
        compiles a complete method
        function or constructor
        :return: None
        """
        # insert <subroutineDec>
        subroutine_dec_element = etree.Element(SUBROUTINE_DEC)

        # <keyword> constructor | function | method </keyword>
        self.insert_next_token(subroutine_dec_element)
        # <keyword> returnType </keyword>
        self.insert_next_token(subroutine_dec_element)
        # <identifier> subroutineName </identifier>
        self.insert_next_token(subroutine_dec_element)

        # start of parameter list
        # <symbol> "(" </symbol>
        self.insert_next_token(subroutine_dec_element)

        # parameter list compilation
        # and inserting it into the subtree
        subroutine_dec_element = self.compile_parameter_list(
            subroutine_dec_element)

        # <symbol> ")" </symbol>
        self.insert_next_token(subroutine_dec_element)
        # end of parameter list

        # as son of subroutine declaration
        subroutine_body = self.compile_subroutine_body()
        subroutine_dec_element.append(subroutine_body)
        # adding all subroutine declaration
        # as trees son

        # insert subroutineDec tree into all the class
        self.root.append(subroutine_dec_element)
        return

    def compile_subroutine_body(self) -> etree:
        """
        method to compile subroutine body
        :return: tree of subroutine
        """
        # insert <subroutineBody>
        subroutine_body_element = etree.Element(SUBROUTINE_BODY)

        # <symbol> "{" </symbol>
        self.insert_next_token(subroutine_body_element)

        current_token = self.tokenizer.get_current_token()[1]

        # read all variable declares
        while CompilationEngine.is_var_declare(current_token):
            # adding var declare subtree
            # to subroutine body element tree
            subroutine_body_element = self.compile_var_declaration(
                subroutine_body_element)
            current_token = self.tokenizer.get_current_token()[1]

        statements_tree = self.compile_statements()

        subroutine_body_element.append(statements_tree)
        # <symbol> "}" </symbol>
        self.insert_next_token(subroutine_body_element)

        return subroutine_body_element

    def compile_var_declaration(self, subroutine_body_element) -> etree:
        """
        method to compile var declaration lines and add to the subroutine
        body tree
        :param subroutine_body_element: tree to add var to
        :return: the new subroutine body element
        """
        # insert <varDec>
        var_dec_tree = etree.Element(VAR_DEC)

        # <keyboard> "var" </keyboard>
        self.insert_next_token(var_dec_tree)
        # <keyboard> varType </keyboard>
        self.insert_next_token(var_dec_tree)

        # <identifier> varName </identifier>
        self.insert_next_token(var_dec_tree)

        # run in a loop and print all names, with "," in between
        while self.tokenizer.current_word == COMMA:
            # <symbol> , </symbol>
            self.insert_next_token(var_dec_tree)
            # <identifier> varName </identifier>
            self.insert_next_token(var_dec_tree)

        # end of declaration
        # <symbol> ; </symbol>
        self.insert_next_token(var_dec_tree)

        subroutine_body_element.append(var_dec_tree)
        # etree.SubElement(self.root, class_var_dec_element)
        return subroutine_body_element

    def compile_parameter_list(self, subroutine_dec_element: etree) -> etree:
        """
        compiles a (CAN BE EMPTY) parameter list
        not including the enclosing "()"
        :return: etree
        """
        param_list_element = etree.Element(PARAM_LIST)
        current_token = self.tokenizer.get_current_token()[1]

        # till we at the end of the param line -> ")"
        if current_token != END_OF_PARAM_LIST:

            # <identifier> varType </identifier>
            self.insert_next_token(param_list_element)
            # <identifier> varName </identifier>
            self.insert_next_token(param_list_element)

            current_token = self.tokenizer.get_current_token()[1]

            # go through param list
            while current_token == COMMA:
                # <symbol> , </symbol>
                self.insert_next_token(param_list_element)
                # <identifier> varType </identifier>
                self.insert_next_token(param_list_element)
                # <identifier> varName </identifier>
                self.insert_next_token(param_list_element)

                # renew current token
                current_token = self.tokenizer.get_current_token()[1]
        else:
            # it is an empty list
            # check to prevent deletion of tag
            for elem in param_list_element.iter():
                if elem.text is None:
                    elem.text = '\n'
        subroutine_dec_element.append(param_list_element)
        return subroutine_dec_element

    def compile_statements(self) -> etree:
        """
        compiles a sequence of statements
        not including the enclosing {}
        :return: tree of statements
        """
        # insert <statements>
        statements_body = etree.Element(STATEMENTS)
        current_token = self.tokenizer.get_current_token()[1]

        if current_token == END_OF_CLASS:
            for elem in statements_body.iter():
                if elem.text is None:
                    elem.text = '\n'
            return statements_body

        # read statements as long as we have them
        # determine their type
        # add the statement block to the
        # over all statements blocks
        # as subtrees
        while CompilationEngine.is_statement(current_token):
            current_statement_tree = None
            # pretty much straight forward
            # we have some types of statements
            # and we need to find out which one
            # and send to the fitting compilation method
            if current_token == LET:
                current_statement_tree = self.compile_let()
            elif current_token == IF:
                current_statement_tree = self.compile_if()
            elif current_token == WHILE:
                current_statement_tree = self.compile_while()
            elif current_token == DO:
                current_statement_tree = self.compile_do()
            elif current_token == RETURN:
                current_statement_tree = self.compile_return()
            # adding the statement
            statements_body.append(current_statement_tree)
            # getting the token we are on
            current_token = self.tokenizer.get_current_token()[1]
        return statements_body

    def compile_do(self) -> etree:
        """
        compiles a do statement
        :return: None
        """
        # insert <doStatement>
        do_statement_body = etree.Element(DO + STATEMENT_STR)

        # insert <keyword> do </keyword>
        self.insert_next_token(do_statement_body)

        # insert <identifier> subroutineName </identifier>
        # ------- or, for another class method  ---------
        # insert <identifier> className </identifier>
        self.insert_next_token(do_statement_body)

        current_token = self.tokenizer.get_current_token()[1]
        if current_token == DOT:
            # it is a call for a className.subroutineName
            # insert <symbol> . </symbol>
            self.insert_next_token(do_statement_body)
            # insert <identifier> subroutineName </identifier>
            self.insert_next_token(do_statement_body)

        # elif current_token == START_OF_PARAM_LIST:
        # we immediately proceed to "(" -> expression list -> ")"

        # start of expression list
        # ------------------------
        # insert <symbol> ( </symbol>
        self.insert_next_token(do_statement_body)

        # compilation of expression list
        expression_list_tree = self.compile_expression_list()
        # add expression list tree to do statement body
        do_statement_body.append(expression_list_tree)

        # insert <symbol> ) </symbol>
        self.insert_next_token(do_statement_body)
        # ------------------------
        # end of expression list

        # insert <symbol> ; </symbol>
        self.insert_next_token(do_statement_body)
        return do_statement_body

    def compile_let(self) -> etree:
        """
        compiles a let statement
        --------------------
        let  "var_name" = "expression" ;
        --------------------
        :return: tree of a let statement
        """
        # insert <letStatement>
        let_statement_body = etree.Element(LET + STATEMENT_STR)
        # insert <keyword> let </keyword>
        self.insert_next_token(let_statement_body)

        # should be varName, might be varName []
        # insert <identifier> varName </identifier>
        self.insert_next_token(let_statement_body)

        current_token = self.tokenizer.get_current_token()[1]
        if current_token == ARRAY_OPENER:
            # insert <symbol> [ </symbol>
            self.insert_next_token(let_statement_body)
            # create expression tree
            expression_sub_tree = self.compile_expression()
            # add subtree of expression to let statement tree
            let_statement_body.append(expression_sub_tree)
            # insert <symbol> ] </symbol>
            self.insert_next_token(let_statement_body)

        # should be =
        # insert <symbol> = </symbol>
        self.insert_next_token(let_statement_body)

        # expression right of equality
        expression_sub_tree = self.compile_expression()
        # add subtree of expression to let statement tree
        let_statement_body.append(expression_sub_tree)

        # insert <symbol> ; </symbol>
        self.insert_next_token(let_statement_body)
        return let_statement_body

    def compile_while(self) -> etree:
        """
        compiles a while statement
        --------------------
        while  ( "expression" )
        { "statements }
        --------------------
        :return: tree of a while statement
        """
        # insert <whileStatement>
        while_statement_body = etree.Element(WHILE + STATEMENT_STR)
        # insert <keyword> while </keyword>
        self.insert_next_token(while_statement_body)

        # insert <symbol> ( </symbol>
        self.insert_next_token(while_statement_body)

        # expression of while
        expression_tree = self.compile_expression()
        while_statement_body.append(expression_tree)

        # insert <symbol> ) </symbol>
        self.insert_next_token(while_statement_body)

        # insert <symbol> { </symbol>
        self.insert_next_token(while_statement_body)

        statements_tree = self.compile_statements()
        while_statement_body.append(statements_tree)

        # insert <symbol> } </symbol>
        self.insert_next_token(while_statement_body)
        return while_statement_body

    def compile_return(self) -> etree:
        """
        compiles a return statement
        :return: tree of return statement
        """
        # insert <returnStatement>
        return_statement_body = etree.Element(RETURN + STATEMENT_STR)

        # insert <keyword> return </keyword>
        self.insert_next_token(return_statement_body)

        current_token = self.tokenizer.get_current_token()[1]
        if current_token != COMMA_DOT:
            expression_tree = self.compile_expression()
            return_statement_body.append(expression_tree)

        # insert <symbol> ; </keyword>
        self.insert_next_token(return_statement_body)
        return return_statement_body

    def compile_if(self) -> etree:
        """
        compiles an if statement
        possibly with a trailing else clause
        --------------------
        if  ( "expression" )
        { "statements }
        --------------------
        :return: tree of an if statement
        """
        # insert <ifStatement>
        if_statement_body = etree.Element(IF + STATEMENT_STR)

        # insert <keyword> if </keyword>
        self.insert_next_token(if_statement_body)
        # insert <symbol> ( </symbol>
        self.insert_next_token(if_statement_body)

        # build if expression
        if_expression_tree = self.compile_expression()
        if_statement_body.append(if_expression_tree)

        # insert <symbol> ) </symbol>
        self.insert_next_token(if_statement_body)

        # insert <symbol> { </symbol>
        self.insert_next_token(if_statement_body)

        # insert whats inside if() { lalla }
        if_body_tree = self.compile_statements()
        if_statement_body.append(if_body_tree)

        # insert <symbol> } </symbol>
        self.insert_next_token(if_statement_body)

        # now we might have else:
        current_token = self.tokenizer.get_current_token()[1]
        if current_token == ELSE:
            # insert <keyword> else </keyword>
            self.insert_next_token(if_statement_body)
            # insert <symbol> { </symbol>
            self.insert_next_token(if_statement_body)

            else_body_tree = self.compile_statements()
            if_statement_body.append(else_body_tree)

            # insert <symbol> } </symbol>
            self.insert_next_token(if_statement_body)

        return if_statement_body

    def compile_expression(self) -> etree:
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
        # insert <expression>
        expression_list_body = etree.Element(EXPRESSION)

        # first term
        term_body = self.compile_term()
        expression_list_body.append(term_body)

        current_token = self.tokenizer.get_current_token()[1]
        while current_token in BINARY_OPERATORS:
            # <symbol> binaryOp </symbol>
            self.insert_next_token(expression_list_body)

            # compile term
            term_body = self.compile_term()

            # add <term> lalala </term>
            expression_list_body.append(term_body)

            # renew again
            current_token = self.tokenizer.get_current_token()[1]

        return expression_list_body

    def compile_term(self) -> etree:
        """
        compiles a term.
        if the current token is an identifier  we distinguish between
        - a variable: .
        - an array entry: [
        - subroutine call: (
        :return: tree of term
        """
        # insert <term>
        term_body = etree.Element(TERM)

        # get current token we insert
        current_token = self.tokenizer.get_current_token()
        token_type = current_token[0]
        token_string = current_token[1]

        # integerConstant | stringConstant | keywordConstant
        if (token_type == JackTokenizer.INT_TYPE) | (
                token_type == JackTokenizer.STRING_TYPE) | (
                token_type == JackTokenizer.KEYWORD_TYPE):
            self.insert_next_token(term_body)
        # unaryOperator {- , ~}
        elif token_string in UNARY_OPERATORS:
            self.insert_next_token(term_body)
            # create a term of the inside of the operator
            sub_term_body = self.compile_term()
            # and append it to the term_body
            term_body.append(sub_term_body)
        # start of another expression
        elif token_string == START_OF_PARAM_LIST:
            # insert <symbol> ( </symbol>
            self.insert_next_token(term_body)
            # insert expression
            sub_expression = self.compile_expression()
            term_body.append(sub_expression)
            # insert <symbol> ) </symbol>
            self.insert_next_token(term_body)
        # anyways we have a varName or, varName[] or, subroutineCall ()
        else:
            # varName
            # or subroutineCall
            self.insert_next_token(term_body)
            possibly_parent = self.tokenizer.get_current_token()[1]
            # pretty much straight forward:
            # 1. array opener []
            # 2. call of subroutineName()
            # 3. className. -> and then # 2. call of subroutineName()
            # 4. simple varName -> handled in project 11
            if possibly_parent == ARRAY_OPENER:
                # insert <symbol> [ </symbol>
                self.insert_next_token(term_body)
                # expression inside []
                inside_expression = self.compile_expression()
                # adding it to tree
                term_body.append(inside_expression)
                # insert <symbol> ] </symbol>
                self.insert_next_token(term_body)
            elif possibly_parent == START_OF_PARAM_LIST:
                # subroutine call immediately
                # <symbol> ( </symbol>
                self.insert_next_token(term_body)
                # get expression list:
                expression_list = self.compile_expression_list()
                # append it to tree
                term_body.append(expression_list)
                # <symbol> ) </symbol>
                self.insert_next_token(term_body)
            elif possibly_parent == DOT:
                # we have a className.
                # now we will have a subroutine name and call

                # <symbol> . </symbol>
                self.insert_next_token(term_body)

                # <identifier> subroutineName </identifier>
                self.insert_next_token(term_body)

                # <symbol> ( </symbol>
                self.insert_next_token(term_body)
                # get expression list:
                expression_list = self.compile_expression_list()
                # append it to tree
                term_body.append(expression_list)
                # <symbol> ) </symbol>
                self.insert_next_token(term_body)
        return term_body

    def compile_expression_list(self) -> etree:
        """
        compiles (might be empty list) a comma separated
        list of expression
        :return: tree of expression list
        """
        # insert <expressionList>
        expression_list_body = etree.Element(EXPRESSION_LIST)

        # we start unless we are already at ")"
        # just like with param list

        current_token = self.tokenizer.get_current_token()[1]

        if current_token != END_OF_PARAM_LIST:

            current_expression_tree = self.compile_expression()
            expression_list_body.append(current_expression_tree)
            # renew current token
            current_token = self.tokenizer.get_current_token()[1]

            while current_token == COMMA:
                # <symbol> , </symbol>
                self.insert_next_token(expression_list_body)
                # new expression tree
                current_expression_tree = self.compile_expression()
                # inserting it into the current tree
                expression_list_body.append(current_expression_tree)
                # and go again, renew current token
                current_token = self.tokenizer.get_current_token()[1]
        else:
            # check to prevent deletion of tag
            for elem in expression_list_body.iter():
                if elem.text is None:
                    elem.text = '\n'
        return expression_list_body
