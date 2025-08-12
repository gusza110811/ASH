import type
from typing import TYPE_CHECKING
import math

def get_global(mem:"ash.Memory"):
    mem.set("print", type.python("print(args[0].ref())",mem))
    mem.set("square", type.python("args[0].ref()**2",mem))
    mem.set("add", type.python("args[0].ref()+args[1].ref()",mem))
    mem.set("pi", type.num(math.pi,mem))
    mem.set("version", type.string("DEV.-",mem))

if TYPE_CHECKING:
    import ash