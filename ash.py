from __future__ import annotations
import os
import sys
import re

import builtin
from utils import Utils
from memory import *
from type import *

class Shell:
    def __init__(self,executor:Executor):
        self.executor = executor
        return

    def c(self):
        print("ASH developmental build (c) 2025 S. \"Gusza\" N.")

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


class Executor:
    def __init__(self, parser:Parser, memory:Memory):
        self.parser = parser
        self.memory = memory

    def executelineparsed(self, expr:obj):

        def caller(expr:call):
            # check if any of the parameters are function to be called
            for idx, param in enumerate(expr.params):
                if isinstance(param,call):
                    expr.params[idx] = caller(param)
                elif isinstance(param,reference):
                    expr.params[idx] = param.ref(mem=self.memory)

            result = expr.call(self.memory)
            return self.parser.utils.pytype_to_ash_type(result)

        if isinstance(expr,call) or isinstance(expr,assignment):
            return caller(expr)
        else:
            return expr

    def execute(self, code:str):
        parsed = self.parser.parse(code,self.memory)
        for idx, line in enumerate(parsed):
            #try:
                result = self.executelineparsed(line)
                if result is not None:
                    print(result.ref())
            #except Exception as e:
            #    return e, idx, line
        
        return None, None, None

class Parser:
    def __init__(self,utils:Utils):
        self.utils = utils
        return

    def parse(self,line:str,mem:Memory,executor:Executor=None):
        if not line.endswith(";"):
            line += ";"

        words:list[str] = re.split(r"(\s+)", line)
        tokens:list[obj]=[]
        tokensline:list[obj]=[]

        # symbol separator
        tmp = words
        words = []
        symbols = list("{}[]()<>+-=*&^|/:;,")
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
            if not token.strip():
                continue

            # double quote string
            if token.startswith('"'):
                while not token.endswith('"'):
                    token += words.pop(0)
                    if token.endswith(";"):
                        raise SyntaxError('String literal not closed')
                tokensline.append(string(token[1:-1],mem))

            # single quote string
            elif token.startswith("'"):
                while not token.endswith("'"):
                    token += words.pop(0)
                    if token.endswith(";"):
                        raise SyntaxError('String literal not closed')
                tokensline.append(string(token[1:-1],mem))
            
            # number
            elif self.utils.can_num(token):
                token = float(token)
                tokensline.append(num(token,mem))

            # assignment
            elif token == "=":
                if len(tokensline) > 1:
                    raise SyntaxError("Too many target to assign to")
                unparsedvalue = ""
                newwords=words.copy()
                for _word in words:
                    if _word != ";":
                        unparsedvalue += _word
                        newwords.pop(0)
                    else:
                        break
                name = tokensline.pop(0)
                mem.set(name.name, obj())
                value = self.parse(unparsedvalue, mem)[0]
                tokensline.append(assignment([name, value],mem))
                words = newwords
            
            # accessing local things
            elif token == ":":
                if len(tokensline) == 0:
                    raise SyntaxError("Unexpected /")
                parent = tokensline.pop(0)
                if isinstance(parent,reference):
                    parent = parent.ref(mem)
                child = words.pop(0)
                result = reference(child,parent.local)
                tokensline.append(result)

            # array
            elif token.startswith("("):
                # collect everything inside the matching parentheses into inner_tokensline
                inner_tokens = []
                depth = 1  # we already saw the opening "("
                while len(words) != 0 and depth > 0:
                    w = words.pop(0)
                    if w == "(":
                        depth += 1
                    elif w == ")":
                        depth -= 1

                    # only append tokensline that are *inside* the outer parentheses
                    if depth > 0:
                        inner_tokens.append(w)

                if depth != 0:
                    raise SyntaxError("Unmatched '('")

                # split inner_tokensline into top-level args on commas (ignore commas in nested brackets)
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
                tokensline.append(array(parsed_args,mem))
            
            elif token == ";":
                # interpret calls
                idx = -1
                while idx < len(tokensline)-1:
                    idx+=1
                    token = tokensline[idx]
                    try:
                        if not isinstance(token,reference):
                            continue

                        token2 = tokensline[idx+1]
                        if not isinstance(token2,array): raise IndexError # does not make sense but idrc lol
                        tokensline[idx] = call([token.ref(mem=token.local.parent),token2.ref()],mem)
                        tokensline.pop(idx+1)
                    except IndexError:
                        continue
                if len(tokensline) > 1:
                    print(tokensline)
                    raise SyntaxError("Too many expressions in one line")

                tokens.append(tokensline[0])
                tokensline = []

            else:
                if mem.exists(token):
                    tokensline.append(reference(token,mem))
                else:
                    tokensline.append(undefined(token,mem))

        return tokens


if __name__ == "__main__":
    memory = Memory()
    utils = Utils(memory)
    builtin.get_global(memory)
    parser = Parser(utils)
    executor = Executor(parser,memory)
    shell = Shell(executor)

    shell.c()
    try:
        shell.main()
    finally:
        utils.dump_mem(executor.memory)
