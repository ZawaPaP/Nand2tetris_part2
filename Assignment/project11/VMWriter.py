from JackTokenizer import JackTokenizer
import sys
import os
import glob

class VMWriter():
    def __init__(self, outputfile):
        self.outputfile = outputfile
        self.tempNumber = 0

    def Constructor(self,file):
        file_name = os.path.basename(file).split(".")[0]
        ext_name = ".vm"
        dir_name = os.path.dirname(file).replace('./', '')
        #print(file_name)
        #print(dir_name)
        # create subdirectory for compiled
        os.makedirs("./{}".format(dir_name), exist_ok=True)
        #return "./compiled/{}/{}{}".format(dir_name, file_name, ext_name)
        outputfile_name = "./{}/{}{}".format(dir_name, file_name, ext_name)
        self.outputfile = open(outputfile_name, 'w')
        return self.outputfile

    def writePush(self, segment, index):
        #print("write push")
        self.outputfile.write("push " + segment +" "+ str(index) + "\n")

    def writePop(self, segment, index):
        #print("write pop")
        self.outputfile.write("pop " + segment +" "+ str(index) + "\n")


    def writeArithmetic(self, command):
        #print("write Arithmetic")
        self.outputfile.write(command  + "\n")


    def writeLabel(self, label):
        #print("write label")
        self.outputfile.write("label " + label  + "\n")

    def writeGoto(self, label):
        #print("write goto")
        self.outputfile.write("goto " + label  + "\n")

    def writeIf(self, label):
        #print("write if")
        self.outputfile.write("if-goto " + label  + "\n")

    def writeCall(self, name, nArgs):
        #print("write call")
        self.outputfile.write("call " + name +" "+ str(nArgs) + "\n")


    def writeFunction(self, name, nLocals):
        print(self.outputfile)
        #print("write function")
        self.outputfile.write("function " + name +" "+ str(nLocals) + "\n")


    def writeReturn(self):
        self.outputfile.write("return\n")

    def close(self):
        self.outputfile.close()
