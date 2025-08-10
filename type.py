import typing

class obj:
    def __init__(self,data=None):
        if data:
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

class string(obj):
    def __init__(self, data):
        super().__init__(data)

class num(obj):
    def __init__(self, data):
        super().__init__(data)
    
    def ref(self):
        if self.data == int(self.data):
            return int(self.data) # return as int if there is no fractional value
        else:
            return self.data

class boolean(obj):
    def __init__(self, data):
        super().__init__(data)
class true(boolean):
    def __init__(self):super().__init__(True)
class false(boolean):
    def __init__(self):super().__init__(False)