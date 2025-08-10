import typing

class obj:
    def __init__(self,data=None):
        if data is not None:
            self.data = data
        else:
            self.data = self
        return
    
    def ref(self): # when the object is referenced. ie. `foo`
        return self.data

    def call(self, args:list): # when the object is called . ie. `foo()`
        return

class python(obj):
    def __init__(self, data):
        super().__init__(data)

    def call(self,args):
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
    
    def call(self,param):
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

# if the token doesnt match anything above, i.e function name, variables etc
class reference(obj):
    def __init__(self, data:obj):
        super().__init__(data)