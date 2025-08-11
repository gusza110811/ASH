import type
from typing import TYPE_CHECKING
import math

def get_global(mem:"gsh.Memory"):
    mem.set("print", type.python("print(args[0].ref())"))
    mem.set("square", type.python("args[0].ref()**2"))
    mem.set("pi", type.num(math.pi))

if TYPE_CHECKING:
    import gsh