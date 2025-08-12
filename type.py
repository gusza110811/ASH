import typing
from typing import TYPE_CHECKING

class obj:
    def __init__(self,data=None):
        if data is not None:
            self.data = data
        else:
            self.data = self
        return
    
    def ref(self,mem:"ash.Memory"=None): # when the object is referenced. ie. `foo`
        return self.data

    def call(self, args:list, mem:"ash.Memory") -> typing.Any: # when the object is called . ie. `foo()`
        return

class python(obj):
    def __init__(self, data):
        super().__init__(data)

    def call(self,args,mem):
        return eval(self.data,{"args":args})

class num(obj):
    def __init__(self, data:int|float):
        super().__init__(data)
    
    def ref(self):
        if self.data == int(self.data):
            return int(self.data) # return as int if there is no fractional value
        else:
            return self.data

class array(obj):
    def __init__(self, data:typing.Iterable):
        super().__init__(data)

    def call(self,param:list[num],mem):
        idx = param[0].ref()
        try:
            idx2 = param[1].ref()
            return self.data[idx:idx2]
        except IndexError:
            return self.data[idx]

class string(array):
    def __init__(self, data:str):
        super().__init__(data)

class boolean(obj):
    def __init__(self, data:bool):
        super().__init__(data)


### Things that have hidden the fact that its just like regular objects
class meta(obj):
    def __init__(self, data):
        super().__init__(data)

class call(meta):
    def __init__(self, data:list[obj,list[obj]]):
        self.name = data[0]
        self.params = data[1]
        super().__init__(data)

    def call(self, mem):
        return self.name.call(self.params,mem)

# placeholder if the token doesnt match anything above, i.e function name, variables etc
class reference(meta):
    def __init__(self, data:str):
        self.name = data
        super().__init__(data)
    
    def ref(self,mem):
        return mem.get(self.name)

    def get_name(self):
        return self.name

# soon-to-be or never-to-be references
class undefined(reference): # inherits reference just because it does similar job
    def __init__(self, data:str):
        self.name = data

    def ref(self):
        raise NameError(f"{self.name} is not defined")

class assignment(meta):
    def __init__(self, data: list[undefined|reference|obj]):
        self.name = data[0].get_name()
        self.params = [data[1]]

    def call(self, mem:"ash.Memory"):
        mem.set(self.name, self.params[0])
        return

if TYPE_CHECKING:
    import ash
