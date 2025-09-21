import re
import type
from collections import deque
from memory import Memory
from utils import Utils

class Parser:
    def __init__(self, utils):
        self.utils = utils

    def parse(self, regex:list, separator="\n", forceSingleItem=False):
        result = []
        item = []

        regex:deque = deque(regex)

        while regex:
            ritem:str = regex.popleft()

            # --- string literal ---
            if ritem == '"':
                buf = []
                while regex and regex[0] != '"':
                    buf.append(regex.popleft())
                if not regex:
                    raise SyntaxError("Unterminated string literal")
                regex.popleft()  # consume closing "
                item.append(type.Literal("string", "".join(buf)))

            elif ritem == "'":
                buf = []
                while regex and regex[0] != "'":
                    buf.append(regex.popleft())
                if not regex:
                    raise SyntaxError("Unterminated string literal")
                regex.popleft()  # consume closing '
                item.append(type.Literal("string", "".join(buf)))

            # --- array literal ( ... ) ---
            elif ritem == "(":
                sub = []
                depth = 1
                while regex and depth > 0:
                    tok = regex.popleft()
                    if tok == "(":
                        depth += 1
                        sub.append(tok)
                    elif tok == ")":
                        depth -= 1
                        if depth > 0:
                            sub.append(tok)
                    else:
                        sub.append(tok)
                if depth != 0:
                    raise SyntaxError("Unterminated array literal")
                if len(item) < 1:
                    item.append(type.Literal("array",
                        self.parse(sub, separator=",", forceSingleItem=True)
                    ))
                else:
                    item.append(
                        type.Call(
                            item.pop(),
                            type.Literal("array",self.parse(sub, separator=",", forceSingleItem=True)))
                        )

            # --- numbers ---
            elif self.utils.can_num(ritem):
                item.append(type.Literal("number", float(ritem)))

            # --- booleans ---
            elif ritem == "true":
                item.append(type.Literal("boolean", True))
            elif ritem == "false":
                item.append(type.Literal("boolean", False))

            # --- separators (newline, comma, etc.) ---
            elif ritem == separator:
                if not forceSingleItem:
                    result.append(item)
                else:
                    if len(item) > 1:
                        raise SyntaxError(f"Too many expressions: {item}")
                    result.append(item[0])
                item = []

            # --- identifiers (default case) ---
            elif ritem.strip():
                item.append(type.Identifier(ritem))

        # --- flush last item ---
        if item:
            if not forceSingleItem:
                result.append(item)
            else:
                if len(item) > 1:
                    raise SyntaxError(f"Too many expressions: {item}")
                result.append(item[0])

        return result

    def regex(self, script):
        # tokenization: split but keep delimiters
        split = re.split(r"([<>/\\|'\"=\+\-.,(){}*&|^\t\n ])", script)
        return [item for item in split if item]

def print_list(data, indent=0):
    print(f"{'  ' * (indent)}[")
    for item in data:
        if isinstance(item, list):
            print_list(item, indent + 1)
        else:
            print(f"{'  ' * indent} {item}")
    print(f"{'  ' * (indent)}]")

def shell(parser:Parser):
    while 1:
        regex = parser.regex(input("ASH>"))
        parsed = parser.parse(regex)
        print_list(parsed)

if __name__ == "__main__":
    memory = Memory()
    utils = Utils(memory)
    parser = Parser(utils)

    shell(parser)