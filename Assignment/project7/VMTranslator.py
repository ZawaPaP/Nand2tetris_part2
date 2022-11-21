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
import pathlib

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
#        dataline = self.fp.readline()
 #       if dataline == "":
  #          print("EOF")
   #         return False
    #    else:

#        print("dataline: " + self.dataline)
        splitline = self.dataline.split("//")[0]  #remove comment line
#        print("splitline: " + splitline)
        if splitline == "":
            return False
        else:
            self.command = splitline.split() #split for each words

    def commandType(self):
        if self.command:
            return self.command[0]

    def arg1(self):
        if self.command:
            return self.command[1]

    def arg2(self):
        if self.command:
            return self.command[2]

class CodeWriter:
    def __init__(self, filename):
        self.file = filename[:-3]
        self.fp = open(filename, 'w')
        self.nextlabel = 0

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
                trans += "M=D\n"
            else:
                trans += "// segment: pop error\n"
        self.fp.write(trans)

    def close(self):
        self.fp.close()

def main():
    filepath = sys.argv[1][:-3]
    inputfile = filepath + ".vm"
    outputfile = filepath + ".asm"

    parser = Parser(inputfile)
    writer = CodeWriter(outputfile)

    while parser.hasMoreCommands():
        parser.advance()
        command = parser.commandType()
#        print(command)
        if command == "push" or command == "pop":
            writer.WritePushPop(command, parser.arg1(), parser.arg2())
        else:
            writer.writeArithmetic(command)

    writer.close()

if __name__ == "__main__":
  main()
