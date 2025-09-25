import re

# Define token types and their corresponding regular expressions
TOKEN_SPECS = [
    ('NUMBER', r'\d+(.\d+)?'),
    ('STRING', r'"(.*)"'),
    ('STRING', r'\'(.*)\''),
    ('BOOL', r'true|false'),
    ('NIL', r'nil'),

    ('PLUS', r'\+'),
    ('MINUS', r'\-'),
    ('MULTIPLY', r'\*'),
    ('DIVIDE', r'\/'),
    ('FLOOR_DIVIDE', r'\/\/'),

    ('EQUALS', r'=='),
    ('MOREEQUAL', r'>='),
    ('LESSEQUAL', r'<='),
    ('MORE', r'>'),
    ('LESS', r'<'),

    ('AND', r'\&'),
    ('OR', r'\|'),
    ('XOR', r'\^'),
    ('NOT', r'\!'),

    ('LOGICAL_AND', r'and'),
    ('LOGICAL_OR', r'or'),
    ('LOGICAL_XOR', r'xor'),
    ('LOGICAL_NOT', r'not'),

    ('LPAREN', r'\('),
    ('RPAREN', r'\)'),
    ('LBRACK', r'\['),
    ('RBRACK', r'\]'),
    ('LCURLY', r'\{'),
    ('RCURLY', r'\}'),

    ('KEYWORD', r'function|return|end|repeat|until'),

    ('IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_]*'),

    ('NEWLINE', r'\n'),
    ('WHITESPACE', r'\s+'),

    ('ASSIGN', r'='),
]

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {ascii(self.value)})"

class Lexer:
    def __init__(self):
        pass

    def tokenize(self,text):
        pos = 0
        tokens = []
        while pos < len(text):
            match_found = False
            for token_type, pattern in TOKEN_SPECS:
                # Use re.match to match from the current position
                match = re.match(pattern, text[pos:])
                #print(token_type, pattern, "->", match, f"@{pos}/{len(text)}")
                if match:
                    value = match.group(0)
                    if token_type != 'WHITESPACE':  # Ignore whitespace tokens
                        tokens.append(Token(token_type, value))
                    pos += len(value)
                    match_found = True
                    break
            if not match_found:
                raise Exception(f"Illegal character at position {pos}: {text[pos]}")
        return tokens