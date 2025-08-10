import os
from type import *
import builtin

class Shell:
    def __init__(self,parser:"Parser",utils:"Utils",executor:"Executor"):
        self.parser = parser
        self.utils = utils
        self.executor = executor
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
                    print(f"{type(token)}: {token}")

class Executor:
    def __init__(self):
        return

class Parser:
    def __init__(self,utils:"Utils"):
        self.utils = utils
        self.names:dict[obj] = builtin.get_global()
        return

    def parse(self,line:str):
        words = line.strip().split()
        tokens:list[obj]=[]

        # symbol separator
        tmp = words
        words = []
        symbols = list("{}[]()<>+-=*&^|:")
        while len(tmp) != 0:
            word = list(tmp.pop(0))
            new = ""
            while len(word) !=0:
                char = word.pop(0)
                if not(char in symbols):
                    new += char
                else:
                    if new:
                        words.append(new)
                    words.append(char)
                    new = ""
            if new:
                words.append(new)

        # main parser
        while len(words) != 0:
            token = words.pop(0)
            # double quote string
            if token.startswith('"'):
                while not token.endswith('"'):
                    token += " " + words.pop(0)
                tokens.append(string(token[1:-1]))
            # single quote string
            elif token.startswith("'"):
                while not token.endswith("'"):
                    token += words.pop(0)
                tokens.append(string(token[1:-1]))
            elif self.utils.can_num(token):
                token = float(token)
                tokens.append(num(token))
            elif token.startswith("("):
                while not token.endswith(")"):
                    token += words.pop(0)
                token = token[1:-1].split(",")
                for idx, item in enumerate(token):
                    token[idx] = self.parse(item)
                tokens.append(array(token))
            else:
                tokens.append(reference(self.names[token]))

        # interpret references(names)
        idx = -1
        while idx < len(tokens)-1:
            idx+=1
            token = tokens[idx]
            if not isinstance(token,reference):
                continue
            try:
                token2 = tokens[idx+1]
                if not isinstance(token2,array): raise IndexError # does not make sense but idrc lol
                tokens[idx] = lambda: token.ref().call(token2)
                tokens.pop(idx+1)
            except IndexError:
                tokens[idx] = token.ref()
                continue
        return tokens

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
    executor = Executor()
    parser = Parser(utils)
    shell = Shell(parser,utils,executor)

    shell.c()
    shell.main()