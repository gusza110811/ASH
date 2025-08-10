import type
import math

def get_global():
    glob:dict[str:type.obj] = {}
    glob["print"] = type.python("print(args[0].ref())")
    glob["pi"] = type.num(math.pi)

    return glob