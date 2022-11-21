"""
class JackTokenizer {
// Constructor (code omitted)
   hasMoreTokens()
   advance()
   tokenType()
   ...
}

other idea
datalineで読み込んで、splitする。
要素内にsymbolが含まれれば、そこで再度Split
各要素について、Keywordなどに当てはまるかどうかを検証
当てはまらない場合、...
"""

import sys
import os
import re
import glob

# [\s\S]は正規表現で改行を含む任意の1文字

class  JackTokenizer():
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
        '\"': '&quot;',
        '&': '&amp;'
    }

    #COMMENT = "(.*//) | (/\*.*\*/) | ( \*[\s]*＾;)| (.*\*/) | (.*/\*\*) | (.* \* .*^;)"
    COMMENT = "(//.*)|(/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/)|(^(?=.*\*)(?!.*;).*$)|(/\*\*\n)|(.*\*/\n)"
    SYMBOL_PATTERN = "([|{|}|(|)|[|]|\.|,|;|\+|-|\*|/|&|\||<|>|=|~|]|\")"

    def __init__(self, inputfile):
        #print("Start JackTokenizer")
        self.fp = inputfile
        #self.outputfile = outputfile
        self.dataline = ""
        self.bit = ""
        self.tokens = []
        self.command = []
        self.list = []

    def read(self):
        self.dataline = self.fp.readline()
        if self.dataline == "":
            return False
        else:
            return True

    def  Constructor(self):
        #print("Start Constructor")
        # skip whitespace and comments
        while self.read():
            splitline = re.split(self.COMMENT, self.dataline)[0]
            if splitline == "":
                continue
            self.list = splitline.split() #split for each words

            #some words are combined, so separate them and insert to command[]
            self.command = []
            for i in self.list:
                self.command.extend(re.split(self.SYMBOL_PATTERN,i))
                self.command = list(filter(None, self.command))
            #print(self.command)

            # handle "" string
            #print(self.command)
            #print(self.command.count('\"'))
            if self.command.count('\"'):
                string = ""
                string_start = self.command.index('\"')
                string_end = self.command.index('\"', string_start + 1, len(self.command))
                string_length = string_end - string_start
                """
                [0,1,2,",4,5,6,",8...]
                start = 3, end = 7, len = 4
                """
                for i in range(string_length + 1):
                    string = string + ' ' + str(self.command.pop(string_start))

                string = "\"" + string[3:-1] + "\""
                #print("string: " + string)
                self.command.insert(string_start, string)
                #print("self.command: ")
                #print(self.command)

            for k in self.command:
                self.tokens.append(k)
        #print(self.tokens)
            # convert them to "<> XXX <>" and insert into tokens[]
        """
            for j in self.command:
                self.bit = j
                key = self.tokenType()[0]
                word = self.tokenType()[1]
                start_key = self.startSymbol(key)
                end_key = self.endSymbol(key)
                # add token to the end of tokens[]
                self.tokens.append(start_key +" " + word +" "+ end_key)
        """
        #print("End Constructor")


    def hasMoreTokens(self):
        if self.tokens == []:
            #print("EOF")
            return False
        else:
            return True

    def advance(self):
        if self.hasMoreTokens():
            self.token = self.tokens.pop(0)
            ##print(self.token)
            return self.token

    """
    def tokenType(self):
        ##print("start tokenType")
        ##print("self.token " + self.token)
        if self.bit in self.KEYWORD:
            ##print("tokenType keyword")
            word = self.keyword()
            return "KEYWORD", word
        elif self.bit in self.SYMBOL:
            ##print("tokenType Symbol")
            word = self.symbol()
            return "SYMBOL", word
        elif self.bit.isidentifier():
            ##print("tokenType Ident")
            word = self.identifier()
            return "IDENTIFIER", word
        elif self.bit.isdecimal():
            ##print("tokenType Int")
            word = self.intVal()
            return "INT_CONST", word
        elif self.bit == "\".*":
            ##print("tokenType string")
            word = self.stringVal()
            return "STRING_CONST", word
        else:
            ##print("tokenType None")
            return "non defined token type"


    def keyword(self):
        return self.bit.upper()

    def symbol(self):
        return self.SYMBOL[self.bit]

    def identifier(self):
        return self.bit

    def intVal(self):
        return self.bit

    def stringVal(self):
        self.bit = self.bit.split("\"")
        return self.bit

    def startSymbol(self, symbol):
        return ("<" + symbol + ">")

    def endSymbol(self, symbol):
        return ("</" + symbol + ">")


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
    ##print("filename: " + file_name)
    ##print("dirname: " + dir_name)
    # create subdirectory for compiled
    os.makedirs("./compiled/{}".format(dir_name), exist_ok=True)
    return "./compiled/{}/{}{}".format(dir_name, file_name, ext_name)


def main():
    if (sys.argv[1] == None):
        #print("argument error")
    else:
        files = fileHandles()
        for file in files:
            ##print("fileName: " + file)
            outputfile_name = xml_outputfile(file)
            outputfile = open(outputfile_name, 'w')
            inputfile = open(file, 'r')
            jt = JackTokenizer(inputfile, outputfile)
            jt.Constructor()
            while jt.hasMoreTokens():
                jt.advance()
            outputfile.close()

if __name__ == "__main__":
  main()
"""
