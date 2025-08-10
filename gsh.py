import os
from type import *

class Shell:
    def __init__(self,parser:"Parser",utils:"Utils"):
        self.parser = parser
        self.utils = utils
        return

    def c(self):
        print("gSH (c) 2025 XXX \"Gusza\"")
    
    def main(self):
        while True:
            line = input(os.getcwd()+">")
            tokens = self.parser.parse_once(line)

            for idx, token in enumerate(tokens):
                print(f"{type(token)}: {token.ref()}")

class Parser:
    def __init__(self,utils:"Utils"):
        self.utils = utils
        return

    def parse_once(self,line:str): # parse a "line"
        words = line.strip().split()
        tokens:list[obj]=[]
        while len(words) != 0:
            token = words.pop(0)
            # double quote string
            if token.startswith('"'):
                while not token.endswith('"'):
                    token += " " + words.pop(0)
                tokens.append(string(token))
            # single quote string
            elif token.startswith("'"):
                while not token.endswith("'"):
                    token += words.pop(0)
                tokens.append(string(token))
            elif self.utils.can_num(token):
                token = float(token)
                tokens.append(num(token))
        
        return tokens
    
    def parse(self): raise NotImplementedError # supposed to run parse_once for every part of the code separated by semicolon

class Utils:
    def __init__(self):
        return

    def can_num(self,string:str):
        try:
            float(string)
            return True
        except ValueError:
            return False

if __name__ == "__main__":
    utils = Utils()
    parser = Parser(utils)
    shell = Shell(parser,utils)

    shell.c()
    shell.main()