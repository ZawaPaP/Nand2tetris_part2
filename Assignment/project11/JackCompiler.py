from JackTokenizer import JackTokenizer
from CompilationEngine  import CompilationEngine
from VMWriter  import VMWriter

import sys
import os
import glob

class JackCompiler():
    def run(input_file, outputfile):
        tokenizer = JackTokenizer(input_file)
        compiler = CompilationEngine(tokenizer, outputfile)
        compiler.CompileClass()

    def fileHandles():
        arg = sys.argv[1]
        if os.path.isfile(arg):
            files = [arg]
        elif os.path.isdir(arg):
            jack_path = os.path.join(arg, "*.jack")
            files = glob.glob(jack_path)
        return files

def main():
    if (sys.argv[1] == None):
        print("argument error")
    else:
        files = JackCompiler.fileHandles()
        for file in files:
            print("fileName: " + file)
            vm_writer = VMWriter(file)
            inputfile = open(file, 'r')
            outputfile = vm_writer.Constructor(file)
            JackCompiler.run(inputfile, outputfile)
            vm_writer.close()

if __name__ == "__main__":
  main()
