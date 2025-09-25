import argparse
from collections import deque
from memory import Memory
from utils import Utils
import parser as p

def print_list(data, indent=0):
    print(f"{'  ' * (indent)}[")
    for item in data:
        if isinstance(item, list):
            print_list(item, indent + 1)
        else:
            print(f"{'  ' * indent} {item}")
    print(f"{'  ' * (indent)}]")

def shell(lexer:p.Lexer):
    while 1:
        tokens = lexer.tokenize(input("ASH>"))
        print_list(tokens)

if __name__ == "__main__":
    lexer = p.Lexer()
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--source","-s", default="")

    args = argparser.parse_args()
    source = args.source

    if not source:
        shell(lexer)

    code = open(source).read()

    tokens = lexer.tokenize(code)

    print_list(tokens)