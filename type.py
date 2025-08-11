import typing
from typing import TYPE_CHECKING

class obj:
    def __init__(self,data=None):
        if data is not None:
            self.data = data
        else:
            self.data = self
        return
    
    def ref(self): # when the object is referenced. ie. `foo`
        return self.data

    def call(self, args:list, mem:"gsh.Memory"): # when the object is called . ie. `foo()`
        return

class python(obj):
    def __init__(self, data):
        super().__init__(data)

    def call(self,args,mem):
        return eval(self.data,globals={"args":args})

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
    
    def call(self,param,mem):
        idx = param[0]
        try:
            idx2 = param[1]
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

    def call(self, args, mem):
        return self.name.call(self.params,mem)

# placeholder if the token doesnt match anything above, i.e function name, variables etc
class reference(meta):
    def __init__(self, data:obj):
        super().__init__(data)

# soon-to-be or never-to-be references
class undefined(reference):
    def __init__(self, data:str):
        super().__init__(data)
    
    def ref(self):
        raise NameError(f"{self.data} is not defined")

class assignment(meta):
    def __init__(self, data: list[undefined, obj]):
        # data[0] is an undefined (variable name)
        # data[1] is the value object
        super().__init__(data)

    def call(self, args, mem:"gsh.Memory"):
        mem.set(self.data[0], self.data[1])
        return

if TYPE_CHECKING:
    import gsh