import typing
from typing import TYPE_CHECKING
import memory

class obj:
    def __init__(self,data=None,mem:memory.Memory=None):
        if mem:
            self.local = memory.Memory(mem)
        else:
            self.local = memory.Memory()

        if data is not None:
            self.data = data
        else:
            self.data = self
        return
    
    def ref(self,mem:memory.Memory=None): # when the object is referenced. ie. `foo`
        return self.data

    def call(self, args:list, mem:memory.Memory) -> typing.Any: # when the object is called . ie. `foo()`
        return

    def __str__(self):
        return f"<{self.__class__.__name__} : {self.data}>"

class Builtin(obj):
    def __init__(self, data, mem:memory.Memory):
        super().__init__(data, mem)

    def call(self,args,mem):
        return eval(self.data,{"args":args})

class num(obj):
    def __init__(self, data:int|float, mem:memory.Memory):
        super().__init__(data, mem)
        add = Builtin(f"{data}+args[0].ref()",mem)
        sub = Builtin(f"{data}-args[0].ref()",mem)
        mul = Builtin(f"{data}*args[0].ref()",mem)
        tdiv = Builtin(f"{data}/args[0].ref()",mem)
        fdiv = Builtin(f"{data}//args[0].ref()",mem)
        self.local.set("add",add)
        self.local.set("sub",sub)
        self.local.set("mul",mul)
        self.local.set("true_div",tdiv)
        self.local.set("floor_div",fdiv)

    def ref(self):
        if self.data == int(self.data):
            return int(self.data) # return as int if there is no fractional value
        else:
            return self.data

class array(obj):
    def __init__(self, data:typing.Iterable, mem:memory.Memory):
        super().__init__(data, mem)

    def call(self,param:list[num],mem):
        idx = param[0].ref()
        try:
            idx2 = param[1].ref()
            return self.data[idx:idx2]
        except IndexError:
            return self.data[idx]

class string(array):
    def __init__(self, data:str, mem:memory.Memory):
        super().__init__(data, mem)

class boolean(obj):
    def __init__(self, data:bool, mem:memory.Memory):
        super().__init__(data, mem)


if TYPE_CHECKING:
    import ash
