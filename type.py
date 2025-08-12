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
        add = python(f"{data}+args[0]",mem)
        self.local.set("add",add)
    
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
    def __init__(self, data, mem:memory.Memory):
        super().__init__(data, mem)

class call(meta):
    def __init__(self, data:list[obj,list[obj]], mem:memory.Memory):
        self.name = data[0]
        self.params = data[1]
        super().__init__(data, mem)

    def call(self, mem):
        return self.name.call(self.params,mem)

# placeholder if the token doesnt match anything above, i.e function name, variables etc
class reference(meta):
    def __init__(self, data:str, mem:memory.Memory):
        self.name = data
        super().__init__(data, mem)
    
    def ref(self,mem):
        return mem.get(self.name)

    def get_name(self):
        return self.name

# soon-to-be or never-to-be references
class undefined(reference): # inherits reference only because it does similar job
    def __init__(self, data:str, mem:memory.Memory):
        self.name = data

    def ref(self, *args, **kwargs):
        raise NameError(f"{self.name} is not defined")

class assignment(meta):
    def __init__(self, data: list[undefined|reference|obj], mem:memory.Memory):
        self.name = data[0].get_name()
        self.params = [data[1]]

    def call(self, mem:memory.Memory):
        mem.set(self.name, self.params[0])
        return

if TYPE_CHECKING:
    import ash
