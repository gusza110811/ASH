import re

class Parser:
    def __init__(self):
        pass

    def regex(self, script):
        split = re.split(r"([<>/\\|'\"=+-(){}*&|^ ])")

        split = [item for item in split if item]

        return split

if __name__ == "__main__":
    parser = Parser()