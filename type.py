class obj:
    def __init__(self,data):
        self.data = data
        return
    
    def ref(self): # when the object is referenced. ie. `foo`
        return self.data

    def call(self): # when the object is called . ie. `foo()`
        return

class python(obj):
    def __init__(self, data):
        super().__init__(data)
    
    def run(self):
        return eval(self.data)

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