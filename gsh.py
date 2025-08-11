import os
from type import *
import builtin
import sys
import re

class Shell:
    def __init__(self,executor:"Executor"):
        self.executor = executor
        return

    def c(self):
        print("gSH (c) 2025 S. \"Gusza\" N.")

    def main(self):
        while True:
            try:
                line = input(os.getcwd()+">")
            except KeyboardInterrupt:
                sys.exit()

            err, linen, line = self.executor.execute(line)

            if err:
                print(f"At line {linen}, `{line}`:")
                print(f">   {err}")

class Memory:
    def __init__(self, parent=None):
        self.vars: dict[str, obj] = {}
        builtin.get_global(self)

        self.parent = parent  # for nested scopes, optional

    def get(self, name: str):
        if name in self.vars:
            return self.vars[name]
        if self.parent:
            return self.parent.get(name)
        raise NameError(f"'{name}' is not defined")

    def set(self, name: str, value: obj):
        self.vars[name] = value

    def exists(self, name: str) -> bool:
        return name in self.vars or (self.parent and self.parent.exists(name))


class Executor:
    def __init__(self, parser:"Parser", memory:Memory):
        self.parser = parser
        self.memory = memory

    def executeline(self, line:str):
        line = line.strip()
        if not line:
            return

        parsed = self.parser.parse(line,self.memory,self)
        if len(parsed) > 1:
            raise SyntaxError("Multiple expressions in one line")


        expr = parsed[0]
        if isinstance(expr,call) or isinstance(expr,assignment):
            return self.parser.utils.pytype_to_gsh_type(expr.call(memory))
        else:
            return expr

    def execute(self, code:str):
        for idx, line in enumerate(code.replace("\n", ";").split(";")):
            try:
                result = self.executeline(line)
                if result is not None:
                    print(result.ref())
            except Exception as e:
                return e, idx, line
        
        return None, None, None

class Parser:
    def __init__(self,utils:"Utils"):
        self.utils = utils
        return

    def parse(self,line:str,mem:Memory,executor:Executor=None):
        words = re.split(r"(\s+)", line)
        tokens:list[obj]=[]

        # symbol separator
        tmp = words
        words = []
        symbols = list("{}[]()<>+-=*&^|/:,")
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
                    token += words.pop(0)
                tokens.append(string(token[1:-1]))

            # single quote string
            elif token.startswith("'"):
                while not token.endswith("'"):
                    token += words.pop(0)
                tokens.append(string(token[1:-1]))
            
            # number
            elif self.utils.can_num(token):
                token = float(token)
                tokens.append(num(token))

            # assignment
            elif token == "=":
                if len(tokens) > 1:
                    raise SyntaxError("Too many target to assign to")
                value = self.parse("".join(words),mem)[0]
                if isinstance(value,call):
                    value = value.call(mem)
                value = utils.pytype_to_gsh_type(value)
                words = []
                tokens.append(assignment([tokens.pop(),value]))

            # array
            elif token.startswith("("):
                # collect everything inside the matching parentheses into inner_tokens
                inner_tokens = []
                depth = 1  # we already saw the opening "("
                while len(words) != 0 and depth > 0:
                    w = words.pop(0)
                    if w == "(":
                        depth += 1
                    elif w == ")":
                        depth -= 1

                    # only append tokens that are *inside* the outer parentheses
                    if depth > 0:
                        inner_tokens.append(w)

                if depth != 0:
                    raise SyntaxError("Unmatched '('")

                # split inner_tokens into top-level args on commas (ignore commas in nested brackets)
                args_token_lists = []
                cur = []
                nest = 0
                for t in inner_tokens:
                    if t in ("(", "[", "{"):
                        nest += 1
                        cur.append(t)
                    elif t in (")", "]", "}"):
                        nest -= 1
                        cur.append(t)
                    elif t == "," and nest == 0:
                        args_token_lists.append(cur)
                        cur = []
                    else:
                        cur.append(t)
                # final arg (could be empty for empty parens)
                if cur or len(args_token_lists) > 0:
                    args_token_lists.append(cur)

                # parse each argument token list (join back to a string)
                parsed_args = []
                for atoks in args_token_lists:
                    if not atoks:  # empty arg -> maybe no args
                        continue
                    else:
                        arg_str = "".join(atoks)
                        parsed_args.append(self.parse(arg_str,mem)[0])
                tokens.append(array(parsed_args))

            else:
                if mem.exists(token):
                    tokens.append(reference([token,mem.get(token)]))
                else:
                    tokens.append(undefined(token))

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
                tokens[idx] = call([token.ref(),token2.ref()])
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

    def pytype_to_gsh_type(self,value):
        if (isinstance(value,int)) or (isinstance(value,float)):
            return num(value)
        if isinstance(value,str):
            return string(value)
        if isinstance(value,typing.Iterable):
            return array(value)
    
    def gsh_type_to_pytype(self,value):
        return value.ref()

if __name__ == "__main__":
    utils = Utils()
    memory = Memory()
    parser = Parser(utils)
    executor = Executor(parser,memory)
    shell = Shell(executor)

    shell.c()
    shell.main()