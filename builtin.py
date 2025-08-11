import type
from typing import TYPE_CHECKING
import math

def get_global(mem:"gsh.Memory"):
    mem.set("print", type.python("print(args[0].ref())"))
    mem.set("pi", type.num(math.pi))

if TYPE_CHECKING:
    import gsh