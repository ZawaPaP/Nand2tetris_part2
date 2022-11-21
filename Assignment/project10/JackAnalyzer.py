from JackTokenizer import JackTokenizer
from CompilationEngine  import CompilationEngine
import sys
import os
import glob

class JackAnalyzer():
    def run(input_file, output_file):
        tokenizer = JackTokenizer(input_file)
        compiler = CompilationEngine(tokenizer, output_file)
        compiler.CompileClass()


    def fileHandles():
        arg = sys.argv[1]
        if os.path.isfile(arg):
            files = [arg]
        elif os.path.isdir(arg):
            jack_path = os.path.join(arg, "*.jack")
            files = glob.glob(jack_path)
        return files

    def xml_outputfile(file):
        file_name = os.path.basename(file).split(".")[0]
        ext_name = ".xml"
        dir_name = os.path.dirname(file).replace('./', '')
        print(file_name)
        print(dir_name)
        # create subdirectory for compiled
        os.makedirs("./{}".format(dir_name), exist_ok=True)
        #return "./compiled/{}/{}{}".format(dir_name, file_name, ext_name)
        return "./{}/{}{}".format(dir_name, file_name, ext_name)

def main():
    if (sys.argv[1] == None):
        print("argument error")
    else:
        files = JackAnalyzer.fileHandles()
        for file in files:
            #print("fileName: " + file)
            outputfile_name = JackAnalyzer.xml_outputfile(file)
            outputfile = open(outputfile_name, 'w')
            inputfile = open(file, 'r')
            JackAnalyzer.run(inputfile, outputfile)
            outputfile.close()

if __name__ == "__main__":
  main()
