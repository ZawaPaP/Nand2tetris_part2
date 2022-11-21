###
# Open file
# load each row

#pjct7 > Arithmetic Logical Command, Memory access commands(push and pop)

# Parse each VM command into its lexical elements
    #Constructor: Opens the file and ready to parse it
    #hasMoreCommands: Are there more commands in the input?
    #advance: Reads the next command (if hasMoreCommands is Y)

    #commandType: returns: C_ARITHMETIC, C_PUSH, C_POP, pjct8 > C_LABEL, C_GOTO, C_IF, C_FUNCTION, C_RETURN, C_CALL (C_ARITHMATIC is returned for all the arithmetic/ logical commands)
    #arg1 string: returns the first argument of the current command. In the case C_ARITHMATIC, the command itself is returned.
    #arg2 int: only if the current command is C_PUSH, C_POPm C_FUNCTION or C_CALL

# writes the assembly code that implements the parsed command
    # Constructor: opens the output file and gets ready to write on it
    # writeArithmetic: Writes to the output file the assembly code
    # WritePushPop: Writes to the output file where the command is either C_PUSH or C_POP
    #Close: Closes the output file

# Main: drives the process

###
import sys
import os
import glob

class  Parser:
    def __init__(self, filename):
        self.fp = open(filename, 'r')
        self.command = []
        self.dataline = ""

        self.cType = {
            "sub" : "math",
            "add" : "math",
            "neg" : "math",
            "eq"  : "math",
            "gt"  : "math",
            "lt"  : "math",
            "and" : "math",
            "or"  : "math",
            "not" : "math",
            "push" : "push",
            "pop"  : "pop",
            "label" : "label",
            "if-goto" : "if-goto",
            "goto" : "goto",
            "function" : "function",
            "call" : "call",
            "return" : "return"
            }

    def hasMoreCommands(self):
#        self.dataline = self.fp.readline()
 #       print(self.dataline)
#        self.advance()
 #       if not self.dataline:
  #          return False
   #     else:
    #        return True
        self.dataline = self.fp.readline()
        if self.dataline == "":
            print("EOF")
            return False
        else:
            return True

    def advance(self):
        splitline = self.dataline.split("//")[0]  #remove comment line
#        print("splitline: " + splitline)
        if splitline == "":
            return False
        else:
            self.command = splitline.split() #split for each words

    def commandType(self):
        if self.command:
#            print(self.cType.get(self.command[0]))
            return self.cType.get(self.command[0])

    def arg1(self):
        if self.command:
            return self.command[1]

    def arg2(self):
        if self.command:
            return self.command[2]

class CodeWriter:
    def __init__(self, filename, outputfile):
        self.file = filename[:-3]
        self.fp = outputfile
        self.nextlabel = 0
        self.functionName = ""

    def  writeArithmetic(self, commandType):
        trans = ""
        if commandType == "add":
            trans += "@SP\n"
            trans += "M=M-1\n"
            trans += "A=M\n"
            trans += "D=M\n"
            trans += "@SP\n"
            trans += "M=M-1\n"
            trans += "A=M\n"
            trans += "M=D+M\n"
            trans += "@SP\n"
            trans += "M=M+1\n"
        elif commandType == "sub":
            trans += "@SP\n"
            trans += "M=M-1\n"
            trans += "A=M\n"
            trans += "D=M\n"
            trans += "@SP\n"
            trans += "M=M-1\n"
            trans += "A=M\n"
            trans += "M=M-D\n"
            trans += "@SP\n"
            trans += "M=M+1\n"
        elif commandType == "neg":
            trans += "@SP\n"
            trans += "A=M-1\n"
            trans += "M=-M\n"
        elif commandType == "eq":
            label = str(self.nextlabel)
            self.nextlabel += 1
            trans += "@SP\n"
            trans += "M=M-1\n"
            trans += "A=M\n"
            trans += "D=M\n"
            trans += "@SP\n"
            trans += "A=M-1\n"
            trans += "D=M-D\n"
            trans += "M=-1\n"
            trans += "@eqTrue" + label + "\n"
            trans += "D;JEQ\n"
            trans += "@SP\n"
            trans += "A=M-1\n"
            trans += "M=0\n"
            trans += "(eqTrue" + label + ")\n"
        elif commandType == "gt":
            label = str(self.nextlabel)
            self.nextlabel += 1
            trans += "@SP\n"
            trans += "M=M-1\n"
            trans += "A=M\n"
            trans += "D=M\n"
            trans += "@SP\n"
            trans += "A=M-1\n"
            trans += "D=M-D\n"
            trans += "M=-1\n"
            trans += "@gtTrue" + label + "\n"
            trans += "D;JGT\n"
            trans += "@SP\n"
            trans += "A=M-1\n"
            trans += "M=0\n"
            trans += "(gtTrue" + label + ")\n"
        elif commandType == "lt":
            label = str(self.nextlabel)
            self.nextlabel += 1
            trans += "@SP\n"
            trans += "M=M-1\n"
            trans += "A=M\n"
            trans += "D=M\n"
            trans += "@SP\n"
            trans += "A=M-1\n"
            trans += "D=M-D\n"
            trans += "M=-1\n"
            trans += "@ltTrue" + label + "\n"
            trans += "D;JLT\n"
            trans += "@SP\n"
            trans += "A=M-1\n"
            trans += "M=0\n"
            trans += "(ltTrue" + label + ")\n"
        elif commandType == "and":
            trans += "@SP\n"
            trans += "M=M-1\n"
            trans += "A=M\n"
            trans += "D=M\n"
            trans += "@SP\n"
            trans += "A=M-1\n"
            trans += "M=D&M\n"
        elif commandType == "or":
            trans += "@SP\n"
            trans += "M=M-1\n"
            trans += "A=M\n"
            trans += "D=M\n"
            trans += "@SP\n"
            trans += "A=M-1\n"
            trans += "M=D|M\n"
        elif commandType == "not":
            trans += "@SP\n"
            trans += "A=M-1\n"
            trans += "M=!M\n"
        else:
            trans += "// Error for Arithmetic\n"
        self.fp.write(trans)

    def  WritePushPop(self, commandType, segment, index):
        trans = ""
        if commandType == "push":
            trans += "// push " + segment +" "+ index + "\n"
            if segment == "constant":
                trans += "@" + index + "\n"
                trans += "D=A\n"
                trans += "@SP\n"
                trans += "A=M\n"
                trans += "M=D\n"
                trans += "@SP\n"
                trans += "M=M+1\n"
            elif segment == "local":
                trans += "@" + index + "\n"
                trans += "D=A\n"
                trans += "@LCL\n"
                trans += "A=M+D\n"
                trans += "D=M\n"
                trans += "@SP\n"
                trans += "A=M\n"
                trans += "M=D\n"
                trans += "@SP\n"
                trans += "M=M+1\n"
            elif segment == "argument":
                trans += "@" + index + "\n"
                trans += "D=A\n"
                trans += "@ARG\n"
                trans += "A=M+D\n"
                trans += "D=M\n"
                trans += "@SP\n"
                trans += "A=M\n"
                trans += "M=D\n"
                trans += "@SP\n"
                trans += "M=M+1\n"
            elif segment == "this":
                trans += "@" + index + "\n"
                trans += "D=A\n"
                trans += "@THIS\n"
                trans += "A=M+D\n"
                trans += "D=M\n"
                trans += "@SP\n"
                trans += "A=M\n"
                trans += "M=D\n"
                trans += "@SP\n"
                trans += "M=M+1\n"
            elif segment == "that":
                trans += "@" + index + "\n"
                trans += "D=A\n"
                trans += "@THAT\n"
                trans += "A=M+D\n"
                trans += "D=M\n"
                trans += "@SP\n"
                trans += "A=M\n"
                trans += "M=D\n"
                trans += "@SP\n"
                trans += "M=M+1\n"
            elif segment == "static":
                trans += "@" + self.file +"." + index + "\n"
                trans += "D=M\n"
                trans += "@SP\n"
                trans += "A=M\n"
                trans += "M=D\n"
                trans += "@SP\n"
                trans += "M=M+1\n"
            elif segment == "temp":
                trans += "@" + index + "\n"
                trans += "D=A\n"
                trans += "@5\n"
                trans += "A=A+D\n"
                trans += "D=M\n"
                trans += "@SP\n"
                trans += "A=M\n"
                trans += "M=D\n"
                trans += "@SP\n"
                trans += "M=M+1\n"
            elif segment == "pointer":
                if index == 0 or index == "0":
                    trans += "@THIS\n"
                    trans += "D=M\n"
                    trans += "@SP\n"
                    trans += "A=M\n"
                    trans += "M=D\n"
                    trans += "@SP\n"
                    trans += "M=M+1\n"
                else:
                    trans += "@THAT\n"
                    trans += "D=M\n"
                    trans += "@SP\n"
                    trans += "A=M\n"
                    trans += "M=D\n"
                    trans += "@SP\n"
                    trans += "M=M+1\n"
            else:
                trans += "// segment: push error\n"
        elif commandType == "pop":
            trans += "// pop " + segment + index + "\n"
            if segment == "local":
                trans += "@SP\n"
                trans += "M=M-1\n"
                trans += "@" + index + "\n"
                trans += "D=A\n"
                trans += "@LCL\n"
                trans += "D=M+D\n"
                trans += "@13\n"
                trans += "M=D\n"
                trans += "@SP\n"
                trans += "A=M\n"
                trans += "D=M\n"
                trans += "@13\n"
                trans += "A=M\n"
                trans += "M=D\n"
            elif segment == "argument":
                trans += "@SP\n"
                trans += "M=M-1\n"
                trans += "@" + index + "\n"
                trans += "D=A\n"
                trans += "@ARG\n"
                trans += "D=M+D\n"
                trans += "@13\n"
                trans += "M=D\n"
                trans += "@SP\n"
                trans += "A=M\n"
                trans += "D=M\n"
                trans += "@13\n"
                trans += "A=M\n"
                trans += "M=D\n"
            elif segment == "this":
                trans += "@SP\n"
                trans += "M=M-1\n"
                trans += "@" + index + "\n"
                trans += "D=A\n"
                trans += "@THIS\n"
                trans += "D=M+D\n"
                trans += "@13\n"
                trans += "M=D\n"
                trans += "@SP\n"
                trans += "A=M\n"
                trans += "D=M\n"
                trans += "@13\n"
                trans += "A=M\n"
                trans += "M=D\n"
            elif segment == "that":
                trans += "@SP\n"
                trans += "M=M-1\n"
                trans += "@" + index + "\n"
                trans += "D=A\n"
                trans += "@THAT\n"
                trans += "D=M+D\n"
                trans += "@13\n"
                trans += "M=D\n"
                trans += "@SP\n"
                trans += "A=M\n"
                trans += "D=M\n"
                trans += "@13\n"
                trans += "A=M\n"
                trans += "M=D\n"
            elif segment == "temp":
                trans += "@" + index + "\n"
                trans += "D=A\n"
                trans += "@5\n"
                trans += "D=A+D\n"
                trans += "@R13\n"
                trans += "M=D\n"
                trans += "@SP\n"
                trans += "M=M-1\n"
                trans += "A=M\n"
                trans += "D=M\n"
                trans += "@13\n"
                trans += "A=M\n"
                trans += "M=D\n"
            elif segment == "pointer":
                if index == 0 or index == "0":
                    trans += "@SP\n"
                    trans += "M=M-1\n"
                    trans += "@SP\n"
                    trans += "A=M\n"
                    trans += "D=M\n"
                    trans += "@THIS\n"
                    trans += "M=D\n"
                else:
                    trans += "@SP\n"
                    trans += "M=M-1\n"
                    trans += "@SP\n"
                    trans += "A=M\n"
                    trans += "D=M\n"
                    trans += "@THAT\n"
                    trans += "M=D\n"
            elif segment == "static":
                trans += "@SP\n"
                trans += "M=M-1\n"
                trans += "A=M\n"
                trans += "D=M\n"
                trans += "@" + self.file +"." + index + "\n"
                trans += "D;JEQ\n"
            else:
                trans += "// segment: pop error\n"
        self.fp.write(trans)


    def  writeLabel(self, label):
        trans = "// writelabel " + str(label) + "\n"
        trans += "(" + self.functionName + "$" + str(label) + ")\n"
        self.fp.write(trans)

    def  writeIfgoto(self,label):
        trans = "// writeIfgoto " + str(label) + "\n"
        trans += "@SP\n"
        trans += "M=M-1\n"
        trans += "A=M\n"
        trans += "D=M\n"
        trans += "@" + self.functionName + "$" + str(label) + "\n"
        trans += "D;JNE\n"
        self.fp.write(trans)

    def  writeGoto(self, label):
        trans = "// writeGoto " + str(label) + "\n"
        trans += "@" + self.functionName + "$" + str(label)+ "\n"
        trans += "0;JEQ\n"
        self.fp.write(trans)

    def  writeFunction(self, functionName, numVars):
        trans = "// writeFunction " + functionName + "\n"
        numVars = int(numVars)
        self.functionName = functionName
        trans += "(" + self.functionName  +  ")\n"
        count = 0
        while (int(numVars) > 0):
                # push local 0
                trans += "@" + str(count) + "\n"
                trans += "D=A\n"
                trans += "@LCL\n"
                trans += "A=M+D\n"
                trans += "M=0\n"
                trans += "@SP\n"
                trans += "M=M+1\n"
                count += 1
                numVars -= 1
        self.fp.write(trans)

    def  writeCall(self, functionName, numArgs):
        trans = "// writeCall1 " + functionName + "\n"
        self.fp.write(trans)
        self.functionName = functionName
        label = str(self.nextlabel)
        self.nextlabel += 1
        return_address = self.functionName + "$ret." + label
        # push return address onto stack
        self.WritePushPop("push", "constant", return_address)
#        trans += "(" + return_address + ")\n"
#        trans += "D=A\n"
#        trans += "@SP\n"
#        trans += "A=M\n"
#        trans += "M=D\n"
#        trans += "@SP\n"
#        trans += "M=M+1\n"
        # push LCL
        trans = ""
        trans += "@LCL\n"
        trans += "D=M\n"
        trans += "@SP\n"
        trans += "A=M\n"
        trans += "M=D\n"
        trans += "@SP\n"
        trans += "M=M+1\n"
        # push ARG
        trans += "@ARG\n"
        trans += "D=M\n"
        trans += "@SP\n"
        trans += "A=M\n"
        trans += "M=D\n"
        trans += "@SP\n"
        trans += "M=M+1\n"
        # push THIS
        trans += "@THIS\n"
        trans += "D=M\n"
        trans += "@SP\n"
        trans += "A=M\n"
        trans += "M=D\n"
        trans += "@SP\n"
        trans += "M=M+1\n"
        # push THAT
        trans += "@THAT\n"
        trans += "D=M\n"
        trans += "@SP\n"
        trans += "A=M\n"
        trans += "M=D\n"
        trans += "@SP\n"
        trans += "M=M+1\n"
        # ARG = SP - 5 - nArgs / reposition ARG
        trans += "@5\n"
        trans += "D=A\n"
        trans += "@" + str(numArgs) +"\n"
        trans += "D=D+A\n"
        trans += "@SP\n"
        trans += "D=M-D\n"
        trans += "@ARG\n"
        trans += "M=D\n"
        # LCL = SP
        trans += "@SP\n"
        trans += "D=M\n"
        trans += "@LCL\n"
        trans += "M=D\n"
        # goto functionName
        trans += "// write goto " + functionName + "\n"
        trans += "@" + self.functionName + "\n"
        trans += "0;JEQ\n"
        # push return Address and label(returnAddress)
        trans += "@SP\n"
        trans += "D=M\n"
        trans += "@R15\n"
        trans += "A=M\n"
        trans += "M=D\n"
        trans += "(" + return_address + ")\n"
        self.fp.write(trans)

    def  writeReturn(self):
        trans = "// writeReturn\n"
        # use R13 to save endFrame (LCL)
        trans += "@LCL\n"
        trans += "D=M\n"
        trans += "@R13\n"
        trans += "M=D\n"
        # retAddr = *(endFrame - 5) // gets the (endFrame - 5) and insert to R14
        trans += "@5\n"
        trans += "D=A\n"
        trans += "@R13\n"
        trans += "A=M-D\n" # D = endFrame - 5
        trans += "D=M\n"
        trans += "@R14\n"
        trans += "M=D\n" # R14 = endFrame - 5
        # *ARG = pop() // reposition the return value
        trans += "@SP\n"
        trans += "M=M-1\n"
        trans += "A=M\n"
        trans += "D=M\n"
        trans += "@ARG\n"
        trans += "A=M\n"
        trans += "M=D\n"
        # SP = ARG + 1 // reposition AP
        trans += "@ARG\n"
        trans += "D=M\n"
        trans += "@1\n"
        trans += "D=D+A\n"
        trans += "@SP\n"
        trans += "M=D\n"
        # THAT = *(endFrame - 1)
        trans += "@R13\n"
        trans += "D=M\n"
        trans += "@1\n"
        trans += "A=D-A\n"
        trans += "D=M\n"
        trans += "@THAT\n"
        trans += "M=D\n"
        # THIS
        trans += "@R13\n"
        trans += "D=M\n"
        trans += "@2\n"
        trans += "A=D-A\n"
        trans += "D=M\n"
        trans += "@THIS\n"
        trans += "M=D\n"
        # ARG
        trans += "@R13\n"
        trans += "D=M\n"
        trans += "@3\n"
        trans += "A=D-A\n"
        trans += "D=M\n"
        trans += "@ARG\n"
        trans += "M=D\n"
        #LCL
        trans += "@R13\n"
        trans += "D=M\n"
        trans += "@4\n"
        trans += "A=D-A\n"
        trans += "D=M\n"
        trans += "@LCL\n"
        trans += "M=D\n"
        # goto retAddr
        trans += "@14\n"
        trans += "A=M\n"
        trans += "0;JEQ\n"
        self.fp.write(trans)

    def writeInit(self):
        trans = "// Bootstrap code\n"
        trans += "@256\n"
        trans += "D=A\n"
        trans += "@SP\n"
        trans += "M=D\n"
        self.fp.write(trans)
        print()
        self.writeCall("Sys.init", 0)

    def close(self):
        self.fp.close()

def fileHandles():
    fileExtention = sys.argv[1][-3:]
    if fileExtention == ".vm":
        source = "singleFile"
        sourceName = sys.argv[1][:-3]
    else:
        source = "directory"
        sourceName = sys.argv[1]
    return source, sourceName


def codeGenerate(parser, writer):
    while parser.hasMoreCommands():
        parser.advance()
        cType = parser.commandType()
        if cType == "function":
            writer.writeFunction(parser.arg1(), parser.arg2())
        elif cType == "call":
            writer.writeCall(parser.arg1(), parser.arg2())
        elif cType == "return":
            writer.writeReturn()
        elif cType == "push" or cType == "pop":
            writer.WritePushPop(cType, parser.arg1(), parser.arg2())
        elif cType =="math":
            writer.writeArithmetic(parser.command[0])
        elif cType == "label":
            writer.writeLabel(parser.arg1())
        elif cType == "if-goto":
            writer.writeIfgoto(parser.arg1())
        elif cType == "goto":
            writer.writeGoto(parser.arg1())

def main():
    sourceType = fileHandles()
    filepath = sourceType[1]
    fileName = ""
    outputfile = filepath + ".asm"

    if sourceType[0] == "singleFile":
        inputfile = filepath + ".vm"
        parser = Parser(inputfile)
        fileName = filepath
        f = open(outputfile, 'w')
        writer = CodeWriter(fileName, f)
        codeGenerate(parser, writer)
    elif sourceType[0] == "directory":
        path = (filepath+"/*.vm")
        lists = glob.glob(path)
        print(lists)
        outputfile = "./" + filepath + "/" + outputfile
        f = open(outputfile, 'w')
        writer = CodeWriter(fileName, f)
        writer.writeInit()
        for list in lists:
            if os.path.splitext(list)[1] == '.vm':
                parser = Parser(list)
                writer = CodeWriter(list, f)
                codeGenerate(parser, writer)
    else:
        print("Unexpected name")
    writer.close()

if __name__ == "__main__":
  main()
