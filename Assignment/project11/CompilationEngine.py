import re
from SymbolTable import SymbolTable
from VMWriter  import VMWriter

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
    TYPES = ['int', 'char', 'boolean']


    def __init__(self, tokenizer, outputfile):
        #print("Start CompilationEngine")
        self.tokenizer = tokenizer
        self.tokens = []
        self.token = ""
        self.current_token = ""
        self.next_token = ""
        self.compiled_class_name = None
        self.symboltable = SymbolTable()
        self.outputfile = outputfile
        self.vm_writer = VMWriter(outputfile)
        self.local_index = 0
        self.temp_index = 0
        self.nLocals = 0
        self.exp_count = 0
        self.label = 0
        self.pointer = 0
        self.function_type = ""
        self.function_name = "No function Name"

    def CompileClass(self):
        #print(self.symboltable.varCount('field'))
        #self.write_outer_tag(body="class")
        self.tokenizer.Constructor()
        while not self.token == 'class':
            self.token = self.tokenizer.advance()
        self.token = self.tokenizer.advance()
        self.compiled_class_name = self.token

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
                #self.write_token()
                self.token = self.tokenizer.advance()
        # write last token
        #self.write_token()
        #self.write_outer_tag(body="/class")
        #self.symboltable.Constructor()
        #print("end compile class")
        self.symboltable.Constructor()
        return

    def CompileClassVarDec(self):
        #print("start compile class var dec")
        #self.write_outer_tag(body="classVarDec")
        while not self.token == ";":
            #print(self.token)
            if self.token == 'field':
                self.token = self.tokenizer.advance()
                self.get_next_token()
                x = self.symboltable.varCount('field')
                Type = self.current_token
                name = self.next_token
                kind = 'field'
                self.symboltable.define(name, Type,'field', self.symboltable.varCount('field'))
                #print("end define")
                self.token = self.tokenizer.advance()
            elif self.token == 'static':
                self.token = self.tokenizer.advance()
                self.get_next_token()
                Type = self.current_token
                name = self.next_token
                kind = 'static'
                self.symboltable.define(name, Type, 'static', self.symboltable.varCount('static'))
                self.token = self.tokenizer.advance()
            elif self.token == ',':
                self.token = self.tokenizer.advance()
                self.symboltable.define(self.token, Type, kind, self.symboltable.varCount(kind))
                self.token = self.tokenizer.advance()
        #self.write_outer_tag(body="/classVarDec")
        #print("end compile class var dec")


    def CompileSubroutineDec(self) :
        #print("start compilesubroutine dec")
        #self.write_outer_tag(body="subroutineDec")
        self.symboltable.startSubroutine()
        if self.token == 'method':
            self.function_type = 'method'
            self.symboltable.define('this', self.compiled_class_name, 'argument', 0)

        if self.token == 'constructor':
            self.token = self.tokenizer.advance()
            self.token = self.tokenizer.advance()
            self.function_name = self.compiled_class_name + "." + self.token
            self.function_type = 'constructor'
            while not self.token == "}":
                if self.token == "(":
                    #self.write_token()
                    self.token = self.tokenizer.advance()
                    self.CompileParameterList()
                    self.token = self.tokenizer.advance()
                    self.token = self.tokenizer.advance() # self.token = let
                    self.CompileSubroutineBody()
                    self.function_type = ''
                    break
                else:
                    self.token = self.tokenizer.advance()
        else:
            while not self.token == "}":
                if self.token == "(":
                    #self.write_token()
                    self.token = self.tokenizer.advance()
                    self.CompileParameterList()
                if self.token == ")":
                    #self.write_token()
                    self.token = self.tokenizer.advance()
                    self.token = self.tokenizer.advance()
                    self.CompileSubroutineBody()
                    break
                elif self.token == "void" or self.token == "int":
                    self.token = self.tokenizer.advance()
                    self.function_name = self.compiled_class_name + "." + self.token
                else:
                    self.token = self.tokenizer.advance()
        #self.token = } to next
        self.function_type = ''
        self.token = self.tokenizer.advance()
        #self.write_outer_tag(body="/subroutineDec")

    def CompileParameterList(self) :
        #print("start compile parmeter list")

        #self.write_outer_tag(body="parameterList")
        while not self.token == ")":
            if self.token in self.TYPES or self.token == self.compiled_class_name:
                self.get_next_token()
                Type = self.current_token
                name = self.next_token
                kind = 'argument'
                self.symboltable.define(name, Type, kind, self.symboltable.varCount(kind))
                self.token = self.tokenizer.advance()
            else:
                self.token = self.tokenizer.advance()
        #self.write_outer_tag(body="/parameterList")


    def CompileSubroutineBody(self):

        while self.token == "var":
                self.CompileVarDec()

        if self.function_type == "constructor":
            self.vm_writer.writeFunction(self.function_name, 0)
            memory_size = self.symboltable.varCount('field')
            self.vm_writer.writePush('constant ', str(memory_size))
            self.vm_writer.writeArithmetic('call Memory.alloc 1')
            self.vm_writer.writeArithmetic("pop pointer 0")
        elif self.function_type == "method":
            self.nLocals = self.symboltable.varCount('local')
            self.vm_writer.writeFunction(self.function_name, self.nLocals)
            self.vm_writer.writePush('argument', 0)
            self.vm_writer.writePop('pointer',0)
        else:
            self.nLocals = self.symboltable.varCount('local')
            #print("self.nLocals = " + str(self.nLocals))
            self.vm_writer.writeFunction(self.function_name, self.nLocals)

        while not self.token == '}':
            if self.token in self.STATEMENT_TOKENS:
                self.CompileStatements()
            else:
                #self.write_token()
                self.token = self.tokenizer.advance()
        # write "}"
        #self.token = }
        #self.token = self.tokenizer.advance()
        #self.write_outer_tag(body="/subroutineBody")
        #print ("EOSB" + self.token)


    def CompileVarDec(self):
        #print("start compilevar dec")

        #self.write_outer_tag(body="varDec")
        while not self.token == ";":
            self.token = self.tokenizer.advance()
            self.get_next_token()
            self.symboltable.define(self.next_token, self.current_token, 'var', self.symboltable.varCount('local'))
            self.token = self.tokenizer.advance()
            #print("self.token: ")
            while self.token == ",":
                # skip the token ","
                self.token = self.tokenizer.advance()
                self.symboltable.define(self.token, self.current_token, 'var', self.symboltable.varCount('local'))
                self.token = self.tokenizer.advance()
        # write ";"
        #self.write_token()
        self.token = self.tokenizer.advance()
        #self.write_outer_tag(body="/varDec")


    def CompileStatements(self):
        #print("start compilestatement")

        #self.write_outer_tag(body="statements")
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
        #self.write_outer_tag(body="/statements")



    def CompileLet(self):
        #print("start compile let")
        # 'let' <varName> ('[' <expression> ']')? '=' <expression> ';'
        #self.write_outer_tag(body="letStatement")
        #self token = "let"
        self.token = self.tokenizer.advance()
        #self token = "<varName>"
        varName = self.token
        self.get_next_token()
        if self.next_token == "[":
            KindOf = self.symboltable.KindOf(varName)
            IndexOf = self.symboltable.IndexOf(varName)
            self.vm_writer.writePush(KindOf, int(IndexOf))
            self.token = self.next_token
            self.CompileExpression()
            self.vm_writer.writeArithmetic('add')
            self.token = self.tokenizer.advance()
            if self.token == "=":
                self.token = self.tokenizer.advance()
                self.CompileExpression()
                self.vm_writer.writePop('temp', 0)
                self.vm_writer.writePop('pointer', 1)
                self.vm_writer.writePush('temp', 0)
                self.vm_writer.writePop('that', 0)
            else:
                print("unexpected let")
        else:
            self.token = self.next_token
            while not self.token == ";":
                if self.token == "=":
                    #self.write_token()
                    self.token = self.tokenizer.advance()
                    self.CompileExpression()
                    break
                elif self.token == ";":
                    break
                else:
                    self.token = self.tokenizer.advance()

            KindOf = self.symboltable.KindOf(varName)
            IndexOf = self.symboltable.IndexOf(varName)
            if not self.function_type == 'constructor':
                if KindOf == 'field':
                    KindOf = 'this'
                self.vm_writer.writePop(KindOf, int(IndexOf))
            else:
                self.vm_writer.writePop('this ', IndexOf)

        # write ";"
        #print(varName)
        self.token = self.tokenizer.advance()
        #self.write_outer_tag(body="/letStatement")


    def CompileIf(self):
        #self.write_outer_tag(body="ifStatement")
        self.token = self.tokenizer.advance() #if to (
        #self.vm_writer.writeArithmetic("<ifStatement - if>")
        self.token = self.tokenizer.advance() # ( to exp
        self.CompileExpression()
        self.vm_writer.writeArithmetic('not')
        label_L1 = ""
        label_L1 = "IF_EXP" + str(self.label)
        self.label += 1
        self.vm_writer.writeIf(label_L1)
        self.token = self.tokenizer.advance() # ) to {
        #self.vm_writer.writeArithmetic("<ifStatement - statement>")
        self.token = self.tokenizer.advance() # { to statement1
        self.CompileStatements()
        label_L2 = ""
        label_L2 = "IF_EXP" + str(self.label)
        self.label += 1
        self.vm_writer.writeGoto(label_L2)
        self.token = self.tokenizer.advance() # statement } to else or next
        if self.token == "else":
            #self.vm_writer.writeArithmetic("<ifStatement - else>")
            self.vm_writer.writeLabel(label_L1)
            self.token = self.tokenizer.advance() # else to {
            self.token = self.tokenizer.advance() # { to statement2
            self.CompileStatements()
            self.vm_writer.writeLabel(label_L2)
            self.token = self.tokenizer.advance() # } to next
        else:
            self.vm_writer.writeLabel(label_L1)
            self.vm_writer.writeLabel(label_L2)
        #self.write_outer_tag(body="/ifStatement")


    def CompileWhile(self):
        #print("start compiles while ")

        #self.write_outer_tag(body="whileStatement")
        #self.write_token()
        self.token = self.tokenizer.advance()

        if self.token in self.EXPRESSION_START:
            #self.write_token()
            self.token = self.tokenizer.advance()
            label_W1 = ""
            label_W1 = "WHILE_EXP" + str(self.label)
            self.label += 1
            self.vm_writer.writeLabel(label_W1)
            self.CompileExpression()
            # move to  ")"
            #self.write_token()
            self.token = self.tokenizer.advance()
            self.vm_writer.writeArithmetic('not')
            label_W2 = ""
            label_W2 = "WHILE_END" + str(self.label)
            self.label += 1
            self.vm_writer.writeIf(label_W2)
        if self.token == "{":
            #self.write_token()
            self.token = self.tokenizer.advance()
            self.CompileStatements()
            # write  "}"
            #self.write_token()
            #self.token = self.tokenizer.advance()
        self.vm_writer.writeGoto(label_W1)
        self.vm_writer.writeLabel(label_W2)
        """
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
        """
        self.token = self.tokenizer.advance()
        #self.write_outer_tag(body="/whileStatement")

    def CompileDo(self):
        # 'do' (identifier '.')? identifier '(' <expressionList> ')' ';'
        #self.write_outer_tag(body="doStatement")
        caller = ""
        self.exp_count = 0
        while not self.token == ";":
            if self.token == "(":
                #self.write_token()
                self.token = self.tokenizer.advance()
                self.CompileExpressionList()
            elif self.token == 'do':
                #self.write_token()
                self.token = self.tokenizer.advance()
            else:
                caller += self.token
                self.token = self.tokenizer.advance()
        #write ";"
        if not self.function_type == 'constructor':
            if self.function_type == 'method':
                if  not '.' in caller:
                    caller = self.compiled_class_name + '.' + caller
                    self.vm_writer.writePush('pointer', 0)
                    self.vm_writer.writeCall(caller, self.exp_count + 1)
                    self.vm_writer.writePop("temp",self.temp_index)
                elif self.symboltable.TypeOf(caller.split('.')[0]):
                    caller = self.symboltable.TypeOf(caller.split('.')[0]) + '.' + caller.split('.')[1]
                    IndexOf = self.symboltable.IndexOf(caller.split('.')[0])
                    self.vm_writer.writePush('this', IndexOf)
                    self.vm_writer.writeCall(caller, self.exp_count + 1)
                    self.vm_writer.writePop("temp",self.temp_index)
                else:
                    self.vm_writer.writeCall(caller, self.exp_count)
                    self.vm_writer.writePop("temp",self.temp_index)
            elif  self.symboltable.TypeOf(caller.split('.')[0]):
                    IndexOf = self.symboltable.IndexOf(caller.split('.')[0])
                    KindOf = self.symboltable.KindOf(caller.split('.')[0])
                    caller = self.symboltable.TypeOf(caller.split('.')[0]) + '.' + caller.split('.')[1]
                    self.vm_writer.writePush(KindOf, IndexOf)
                    self.vm_writer.writeCall(caller, self.exp_count + 1)
                    self.vm_writer.writePop("temp",self.temp_index)
            else:
                self.vm_writer.writeCall(caller, self.exp_count)
                self.vm_writer.writePop("temp",self.temp_index)
        else:
            self.vm_writer.writePush('pointer', 0)
            caller = self.compiled_class_name + '.' + caller
            self.vm_writer.writeCall(caller, 1)
            self.vm_writer.writePop("temp",self.temp_index)
        #self.token = ";"
        #self.write_token()
        self.token = self.tokenizer.advance()
        #self.write_outer_tag(body="/doStatement")

    def CompileReturn(self):
        #'return' <expression>? ';'
        #self.write_outer_tag(body="returnStatement")

        self.token = self.tokenizer.advance()
        if self.token == 'this':
            self.vm_writer.writePush('pointer', 0)
            self.token = self.tokenizer.advance()
            #self.token == ;
        elif not self.token == ";":
            self.CompileExpression()
            #self.token == ;
        else: #self.token == ;
            self.vm_writer.writePush('constant', 0)
        self.vm_writer.writeReturn()
        # self.token ; to next
        self.token = self.tokenizer.advance()
        #self.write_outer_tag(body="/returnStatement")



    def CompileExpression(self):
        # <term> (('+' | '-' | '*' | '/' | '&' | '|' | '<' | '>' | '=') <term>)
        #self.write_outer_tag(body="expression")
        op_token = ""
        self.CompileTerm()
        while not self.token in self.EXPRESSION_END:
            if self.token in self.OP:
                op_token = self.token
                self.token = self.tokenizer.advance()
            else:
                self.CompileTerm()
        #print(op_token)
        if op_token == "+":
            self.vm_writer.writeArithmetic("add")
        elif op_token == "-":
            self.vm_writer.writeArithmetic("sub")
        elif op_token == "*":
            self.vm_writer.writeCall('Math.multiply', 2)
        elif op_token == "/":
            self.vm_writer.writeCall('Math.divide', 2)
        elif op_token == "&":
            self.vm_writer.writeArithmetic("and")
        elif op_token == "|":
            self.vm_writer.writeArithmetic("or")
        elif op_token == "<":
            self.vm_writer.writeArithmetic("lt")
        elif op_token == ">":
            self.vm_writer.writeArithmetic("gt")
        elif op_token == "=":
            self.vm_writer.writeArithmetic("eq")
            #self.token = self.tokenizer.advance()
        #self.write_outer_tag(body="/expression")


    def CompileTerm(self):
        """
        integerConstant | stringConstant | keywordConstant |
        <varName> | <varName> '[' <expression> ']' | <subroutineCall> |
       '(' <expression> ')' | unaryOp <term>
        """
        #self.write_outer_tag(body="term")
        self.get_next_token()
        #print(self.token)
        # '(' <expression> ')'
        if self.current_token == "(":
            #self.vm_writer.writeArithmetic("<Term - <expression> >")
            #self.token = self.current_token
            #self.write_token()
            self.token = self.next_token
            self.CompileExpression()
            # write "end expression"
            #self.write_token()
            self.token = self.tokenizer.advance()
            #self.write_outer_tag(body="/term")
        # if varname[expression]
        elif re.match('\".*', self.current_token):
            self.token = self.current_token
            self.token = self.token[1:-1]
            length = len(self.token)
            self.vm_writer.writePush('constant', length)
            self.vm_writer.writeCall('String.new', 1)
            for c in self.token:
                self.vm_writer.writePush('constant', ord(c))
                self.vm_writer.writeCall("String.appendChar", 2)
            self.token = self.next_token
        elif self.next_token == "[":
            #self.vm_writer.writeArithmetic("<Term - varName[] >")
            self.token = self.current_token
            KindOf = self.symboltable.KindOf(self.token)
            IndexOf = self.symboltable.IndexOf(self.token)
            self.vm_writer.writePush(KindOf, int(IndexOf))
            self.token = self.tokenizer.advance()
            self.CompileExpression()
            self.vm_writer.writeArithmetic('add')
            self.vm_writer.writePop('pointer', 1)
            self.vm_writer.writePush('that', 0)
            # self.token "]"
            #self.write_token()
            self.token = self.tokenizer.advance()
            #self.write_outer_tag(body="/term")
        # if unary_op
        elif self.current_token in self.UNARY_OP:
            #self.vm_writer.writeArithmetic('< Term - unary>')
            unary_op = self.current_token
            self.token = self.next_token
            if self.token == "(" and unary_op == "~":
                self.CompileTerm()
                self.vm_writer.writeArithmetic('not')
            elif self.token.isdecimal() and unary_op == "-":
                self.vm_writer.writePush("constant", str(self.token))
                self.vm_writer.writeArithmetic('neg')
                self.token = self.tokenizer.advance()
            elif self.token.isidentifier() and unary_op == "~":
                self.CompileTerm()
                self.vm_writer.writeArithmetic('not')
            else:
                self.vm_writer.writeArithmetic('< Term - unary> unexpected error')
                self.vm_writer.writeArithmetic(unary_op)
                self.vm_writer.writeArithmetic(self.token)

                #self.vm_writer.writeArithmetic('no defined unary in term')
            #self.write_outer_tag(body="/term")
        #subroutineCall
        elif self.next_token == "(" or self.next_token == ".":
            ##print("next token" + self.next_token)
            #self.vm_writer.writeArithmetic("<Term - subroutineCall >")
            subroutineCall = ""
            self.token = self.current_token
            subroutineCall += self.token
            self.token = self.next_token
            if self.token == "(":
                #self.write_token()
                self.token = self.tokenizer.advance()
                self.CompileExpressionList()
            # self.token == "."
            while not self.token == "(":
                subroutineCall += self.token
                self.token = self.tokenizer.advance()
            # 2nd expressionList
            #self.write_token()
            self.token = self.tokenizer.advance()
            self.CompileExpressionList()
            self.vm_writer.writeCall(subroutineCall, self.exp_count)
            #self.write_outer_tag(body="/term")
        elif self.current_token == 'true':
            #self.vm_writer.writeArithmetic("<Term - true >")
            self.vm_writer.writePush('constant', 0)
            self.vm_writer.writeArithmetic("not")
            self.token = self.next_token
        elif self.current_token == 'false':
            #self.vm_writer.writeArithmetic("<Term - true >")
            self.vm_writer.writePush('constant', 0)
            self.token = self.next_token
        elif self.current_token.isidentifier():
            #self.vm_writer.writeArithmetic("<Term - isidentifier>")
            # if expression is identifier then
            self.token = self.current_token
            KindOf = self.symboltable.KindOf(self.token)
            IndexOf = self.symboltable.IndexOf(self.token)
            print('check')
            print(self.token)
            print(KindOf)
            if KindOf == 'field':
                KindOf = 'this'
                self.vm_writer.writePush(KindOf, int(IndexOf))
            else:
                self.vm_writer.writePush(KindOf, int(IndexOf))
            self.token = self.next_token
        else:
            #print("push n ")
            #self.vm_writer.writeArithmetic("<Term - isdecimal>")
            self.token = self.current_token
            if self.token.isdecimal():
                self.vm_writer.writePush('constant', self.token)

            self.token = self.next_token
            #self.write_outer_tag(body="/term")


    def CompileExpressionList(self):
        # do Screen.drawRectangle(x, y, x + size, y + size);
        #self.write_outer_tag(body="expressionList")
        self.exp_count = 0
        while not self.token == ")":
            if not self.token == ",":
                self.CompileExpression()
                self.exp_count += 1
                continue
            else:
                self.token = self.tokenizer.advance()
                self.CompileExpression()
                self.exp_count += 1
        #self.write_outer_tag(body="/expressionList")
        # write ")"
        #self.write_token()
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
        self.token = (key + ': ' + word + "\n")

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
        elif self.token in self.UNARY_OP:
            word = self.unary()
            return "symbol", word
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
            word = self.identifier()
            return "identifier", word


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

    def unary(self):
        return self.token
