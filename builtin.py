import type
import math

def get_global() -> dict[type.obj]:
    glob = {}
    glob["print"] = type.python("print(args[0])")
    glob["pi"] = type.num(math.pi)

    return glob