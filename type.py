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

class python(obj):
    def __init__(self, data, mem:memory.Memory):
        super().__init__(data, mem)

    def call(self,args,mem):
        return eval(self.data,{"args":args})

class num(obj):
    def __init__(self, data:int|float, mem:memory.Memory):
        super().__init__(data, mem)
        add = python(f"{data}+args[0].ref()",mem)
        sub = python(f"{data}-args[0].ref()",mem)
        mul = python(f"{data}*args[0].ref()",mem)
        tdiv = python(f"{data}/args[0].ref()",mem)
        fdiv = python(f"{data}//args[0].ref()",mem)
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


### Things that have hidden the fact that its just like regular objects
class meta(obj):
    def __init__(self, data=None, mem:memory.Memory=None):
        super().__init__(data, mem)

class call(meta):
    def __init__(self, data:list[str|list[obj]], mem:memory.Memory):
        self.name:list[str] = data[0]
        self.params:list[obj] = data[1]
        super().__init__(data, mem)

    def call(self, mem:memory.Memory):
        target:obj = mem.get(self.name.pop(0))
        while self.name:
            self.local = target.local
            target = self.local.get(self.name.pop(0))
        result = target.call(self.params,self.local)
        return result

# placeholder if the token doesnt match anything above, i.e function name, variables etc
class reference(meta):
    def __init__(self, data:list[str], mem:memory.Memory):
        self.name = data
        self.local = mem

    def ref(self):
        result:obj = self.local.parent.get(self.name.pop(0))
        while self.name:
            self.local = result.local
            result = self.local.get(self.name.pop(0))
        return result

    def get_name(self):
        return self.name

# soon-to-be or never-to-be references
class undefined(reference): # inherits reference only because it does similar job
    def __init__(self, data:list[str], mem:memory.Memory):
        self.name = data
        super().__init__(data,mem)

    def ref(self, *args, **kwargs):
        if len(self.name) == 1:
            raise NameError(f"{self.name} is not defined")
        else:
            raise NameError(f"{":".join(self.name[:-1])} does not contain {self.name[-1]}")

class assignment(meta):
    def __init__(self, data: list[undefined|reference|obj], mem:memory.Memory):
        self.local = mem
        self.path = data[0].get_name()
        self.params = [data[1]]
        self.name = self.path.pop(0)
        while self.path:
            self.local:memory.Memory = self.local.get(self.name).local
            self.name = self.path.pop(0)
        self.local.set(self.name, obj())

    def call(self, mem:memory.Memory):
        self.local.set(self.name, self.params[0])
        return

if TYPE_CHECKING:
    import ash
