import os
from type import *
import builtin

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
            tokens = self.parser.parse(line)

            for idx, token in enumerate(tokens):
                if isinstance(token,obj):
                    print(f"{type(token)}: {token.ref()}")
                else:
                    print(f"{type(token)}: {token()}")

class Parser:
    def __init__(self,utils:"Utils"):
        self.utils = utils
        self.names:dict[obj] = builtin.get_global()
        return

    def parse(self,line:str):
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
            elif (token.endswith(")")) and (not token.startswith("(")):
                name, params = token[:-1].split("(")
                params = params.split(",")
                for idx, param in enumerate(params):
                    subparser = Parser(self.utils)
                    params[idx] = subparser.parse(param)
                tokens.append(lambda:(self.names[name].call(params)))
            else:
                tokens.append(self.names[token].ref)
        
        return tokens
    
    def parse_lines(self): raise NotImplementedError # supposed to run parse for every part of the code separated by semicolon

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