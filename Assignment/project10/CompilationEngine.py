import re
class  CompilationEngine():
    KEYWORD = [
    'class',
    'constructor',
    'function',
    'method',
    'field',
    'static',
    'var',
    'int',
    'char',
    'boolean',
    'void',
    'true',
    'false',
    'null',
    'this',
    'let',
    'do',
    'if',
    'else',
    'while',
    'return'
    ]

    SYMBOL = {
    '{': '{',
    '}': '}',
    '(':'(',
    ')': ')',
    '[': '[',
    ']': ']',
    '.': '.',
    ',': ',',
    ';': ';',
    '+': '+',
    '-': '-',
    '*': '*',
    '/': '/',
    '|': '|',
    '=': '=',
    '<': '&lt;',
    '>': '&gt;',
    '&': '&amp;'
    }


    STATEMENT_TOKENS = [ 'do', 'let', 'while', 'return', 'if' ]
    CLASS_VAR_DEC_TOKENS = ['static', 'field']
    SUBROUTINE_TOKENS = ['constructor', 'function', 'method']
    OPERATOR = ['+', '-', '*', '/', '&', '|', '<', '>', '=']
    EXPRESSION_START = ['(', '[', '=']
    EXPRESSION_END = [')', ']', ';', ',']
    OP = ['+', '-', '*', '/', '&', '|', '<', '>', '=']
    UNARY_OP = ['-', '~']
    KEYWORD_CONSTANT = ['true', 'false', 'null', 'this']


    def __init__(self, tokenizer, outputfile):
        #print("Start CompilationEngine")
        self.tokenizer = tokenizer
        self.outputfile = outputfile
        self.tokens = []
        self.token = ""
        self.current_token = ""
        self.next_token = ""

    def CompileClass(self):
        #print("start CompileClass")
        self.write_outer_tag(body="class")
        self.tokenizer.Constructor()
        self.token = self.tokenizer.advance()
        while self.tokenizer.hasMoreTokens():
            if self.token in self.CLASS_VAR_DEC_TOKENS:
                self.CompileClassVarDec()
                # move to next token
                self.token = self.tokenizer.advance()
            elif self.token in self.SUBROUTINE_TOKENS:
                self.CompileSubroutineDec()
                continue
            elif self.token == None:
                continue
            else:
                self.write_token()
                self.token = self.tokenizer.advance()
        # write last token
        self.write_token()
        self.write_outer_tag(body="/class")
        ##print("end CompileClass")
        return

    def CompileClassVarDec(self):
        """
        <varDec>
        <keyword> var </keyword>
        <keyword> int </keyword>
        <identifier> i </identifier>
        <symbol> , </symbol>
        <identifier> j </identifier>
        <symbol> ; </symbol>
        </varDec>
        """
        self.write_outer_tag(body="classVarDec")
        while not self.token == ";":
            self.write_token()
            self.token = self.tokenizer.advance()
        # write ";"
        self.write_token()
        self.write_outer_tag(body="/classVarDec")


    def CompileSubroutineDec(self) :
        """
        <subroutineDec>
            function void main ( <parameterList> </parameterList> ) <subroutineBody>{}</subroutineBody>
        </subroutineDec>
        """
        self.write_outer_tag(body="subroutineDec")
        while not self.token == "}":
            if self.token == "(":
                self.write_token()
                self.token = self.tokenizer.advance()
                self.CompileParameterList()
            if self.token == ")":
                self.write_token()
                self.token = self.tokenizer.advance()
                self.CompileSubroutineBody()
                break
            else:
                self.write_token()
                self.token = self.tokenizer.advance()
        self.write_outer_tag(body="/subroutineDec")

    def CompileParameterList(self) :
        """
        function void main (parameterList)
        """
        self.write_outer_tag(body="parameterList")
        while not self.token == ")":
            self.write_token()
            self.token = self.tokenizer.advance()
        self.write_outer_tag(body="/parameterList")


    def CompileSubroutineBody(self):
        self.write_outer_tag(body="subroutineBody")
        while not self.token == "}":
            if self.token == "var":
                self.CompileVarDec()
            elif self.token in self.STATEMENT_TOKENS:
                self.CompileStatements()
            else:
                self.write_token()
                self.token = self.tokenizer.advance()
        # write "}"
        self.write_token()
        self.token = self.tokenizer.advance()
        self.write_outer_tag(body="/subroutineBody")
        #print ("EOSB" + self.token)


    def CompileVarDec(self):
        # var String s;
        self.write_outer_tag(body="varDec")
        while not self.token == ";":
            self.write_token()
            self.token = self.tokenizer.advance()
        # write ";"
        self.write_token()
        self.token = self.tokenizer.advance()
        self.write_outer_tag(body="/varDec")


    def CompileStatements(self):
        self.write_outer_tag(body="statements")
        while not self.token == "}":
            if self.token == "let":
                self.CompileLet()
                continue
            elif self.token == "if":
                self.CompileIf()
                continue
            elif self.token == "while":
                self.CompileWhile()
                continue
            elif self.token == "do":
                self.CompileDo()
                continue
            elif self.token == "return":
                self.CompileReturn()
                continue
            else:
                self.write_token()
                self.token = self.tokenizer.advance()
        self.write_outer_tag(body="/statements")



    def CompileLet(self):
        # 'let' <varName> ('[' <expression> ']')? '=' <expression> ';'
        self.write_outer_tag(body="letStatement")
        while not self.token == ";":
            # ('[' <expression> ']')
            if self.token == "[":
                self.write_token()
                self.token = self.tokenizer.advance()
                self.CompileExpression()
            # '=' <expression>
            if self.token == "=":
                self.write_token()
                self.token = self.tokenizer.advance()
                self.CompileExpression()
            else:
                self.write_token()
                self.token = self.tokenizer.advance()
        # write ";"
        self.write_token()
        self.token = self.tokenizer.advance()
        self.write_outer_tag(body="/letStatement")


    def CompileIf(self):
        """
        'if' '(' <expression> ')' '{' statements> '}'
        ('else' '{' statements> '}')?
        """
        self.write_outer_tag(body="ifStatement")
        self.write_token()
        self.token = self.tokenizer.advance()

        while not self.token == "}":
            if self.token in self.EXPRESSION_START:
                self.write_token()
                self.token = self.tokenizer.advance()
                self.CompileExpression()
                continue
            elif self.token == "{":
                self.write_token()
                self.token = self.tokenizer.advance()
                self.CompileStatements()
            else:
                self.write_token()
                self.token = self.tokenizer.advance()
        # write  "}"
        self.write_token()

        #print("else check" + self.token)
        if self.token == "else":
            while not self.token == "}":
                self.write_token()
                self.token = self.tokenizer.advance()
                # write "{"
                self.write_token()
                self.token = self.tokenizer.advance()
                self.CompileStatements()
            # write  "}"
            self.token = self.tokenizer.advance()
            self.write_token()
        self.token = self.tokenizer.advance()
        self.write_outer_tag(body="/ifStatement")


    def CompileWhile(self):
        """
        'while' '(' <expression> ')' '{' statements> '}'
        ('else' '{' statements> '}')?
        """
        self.write_outer_tag(body="whileStatement")
        self.write_token()
        self.token = self.tokenizer.advance()

        if self.token in self.EXPRESSION_START:
            self.write_token()
            self.token = self.tokenizer.advance()
            self.CompileExpression()
            # move to  ")"
            self.write_token()
            self.token = self.tokenizer.advance()
        if self.token == "{":
            self.write_token()
            self.token = self.tokenizer.advance()
            self.CompileStatements()
            # write  "}"
            self.write_token()
            #self.token = self.tokenizer.advance()

        if self.token == "else":
            self.write_token()
            self.token = self.tokenizer.advance()
            # write "{"
            self.write_token()
            self.token = self.tokenizer.advance()
            self.CompileStatements()
            # write  "}"
            self.token = self.tokenizer.advance()
            self.write_token()
        self.token = self.tokenizer.advance()
        self.write_outer_tag(body="/whileStatement")

    def CompileDo(self):
        # 'do' (identifier '.')? identifier '(' <expressionList> ')' ';'
        self.write_outer_tag(body="doStatement")

        while self.token != ";":
            if self.token == "(":
                self.write_token()
                self.token = self.tokenizer.advance()
                self.CompileExpressionList()
            else:
                self.write_token()
                self.token = self.tokenizer.advance()
        #write ";"
        self.write_token()
        self.token = self.tokenizer.advance()
        self.write_outer_tag(body="/doStatement")

    def CompileReturn(self):
        #'return' <expression>? ';'
        self.write_outer_tag(body="returnStatement")
        self.write_token()
        self.token = self.tokenizer.advance()
        if not self.token == ";":
            self.CompileExpression()

        self.write_token()
        self.token = self.tokenizer.advance()
        self.write_outer_tag(body="/returnStatement")



    def CompileExpression(self):
        # <term> (('+' | '-' | '*' | '/' | '&' | '|' | '<' | '>' | '=') <term>)
        self.write_outer_tag(body="expression")
        while not self.token in self.EXPRESSION_END:
            if self.token in self.OP:
                self.write_token()
                self.token = self.tokenizer.advance()
            else:
                self.CompileTerm()
        self.write_outer_tag(body="/expression")


    def CompileTerm(self):
        """
        integerConstant | stringConstant | keywordConstant |
        <varName> | <varName> '[' <expression> ']' | <subroutineCall> |
       '(' <expression> ')' | unaryOp <term>
        """
        self.write_outer_tag(body="term")
        self.get_next_token()
        # '(' <expression> ')'
        if self.current_token == "(":
            ##print("Term - <expression> ")
            self.token = self.current_token
            self.write_token()
            self.token = self.next_token
            self.CompileExpression()
            # write ")"
            self.write_token()
            self.token = self.tokenizer.advance()
        # if varname[expression]
        elif self.next_token == "[":
            ##print("Term - varName[] ")
            self.token = self.current_token
            self.write_token()
            # write "["
            self.token = self.next_token
            self.write_token()
            self.token = self.tokenizer.advance()
            self.CompileExpression()
            # write "]"
            self.write_token()
            self.token = self.tokenizer.advance()
        #subroutineCall
        elif self.next_token == "(" or self.next_token == ".":
            ##print("next token" + self.next_token)
            ##print("Term - subroutineCall ")
            self.token = self.current_token
            self.write_token()
            self.token = self.next_token
            if self.token == "(":
                self.write_token()
                self.token = self.tokenizer.advance()
                self.CompileExpressionList()
            # self.token == "."
            while not self.token == "(":
                self.write_token()
                self.token = self.tokenizer.advance()
            # 2nd expressionList
            self.write_token()
            self.token = self.tokenizer.advance()
            self.CompileExpressionList()
        else:
            ##print("Term - else ")
            self.token = self.current_token
            self.write_token()
            self.token = self.next_token
        self.write_outer_tag(body="/term")


    def CompileExpressionList(self):
        # do Screen.drawRectangle(x, y, x + size, y + size);
        self.write_outer_tag(body="expressionList")
        while not self.token == ")":
            if not self.token == ",":
                self.CompileExpression()
            else:
                self.write_token()
                self.token = self.tokenizer.advance()
        self.write_outer_tag(body="/expressionList")
        # write ")"
        self.write_token()
        self.token = self.tokenizer.advance()



    def write_outer_tag(self, body):
        self.outputfile.write("<{}>\n".format(body))

    def write_token(self):
        self.convert()
        #print(self.token)
        self.outputfile.write(self.token)

    def get_next_token(self):
        self.current_token = self.token
        self.next_token = self.tokenizer.advance()

    def convert(self):
        convert_word = self.tokenType()
        key = convert_word[0]
        word = convert_word[1]
        #print(convert_word)
        #print(word)
        start_key = self.startSymbol(key)
        end_key = self.endSymbol(key)
        # add token to the end of tokens[]
        self.token = (start_key +" " + word +" "+ end_key)

    def tokenType(self):
        ##print("start tokenType")
        ##print("self.token " + self.token)
        if self.token in self.KEYWORD:
            ##print("tokenType keyword")
            word = self.keyword()
            return "keyword", word
        elif re.compile("\".*").search(self.token):
            #print("tokenType string")
            word = self.stringVal()
            #print(word)
            return "stringConstant", word
        elif self.token in self.SYMBOL:
            ##print("tokenType Symbol")
            word = self.symbol()
            return "symbol", word
        elif self.token.isidentifier():
            ##print("tokenType Ident")
            word = self.identifier()
            return "identifier", word
        elif self.token.isdecimal():
            ##print("tokenType Int")
            word = self.intVal()
            return "integerConstant", word
        else:
            ##print("tokenType None")
            return "non defined token type"


    def keyword(self):
        return self.token

    def symbol(self):
        return self.SYMBOL[self.token]

    def identifier(self):
        return self.token

    def intVal(self):
        return self.token

    def stringVal(self):
        self.token = self.token.strip("\"")
        return self.token

    def startSymbol(self, symbol):
        return ("<" + symbol + ">")

    def endSymbol(self, symbol):
        return ("</" + symbol + ">\n")
