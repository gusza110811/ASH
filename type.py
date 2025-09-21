import typing
import memory

class Obj:
    def __init__(self, data=None, mem:memory.Memory=None):
        self.local = memory.Memory(mem) if mem else memory.Memory()
        self.data = data

    def getValue(self):
        """Return the underlying Python primitive (int, str, etc)."""
        return self.data

    def call(self, args:list, mem:memory.Memory) -> typing.Any:
        """Override for callable objects (functions, arrays, etc)."""
        raise TypeError(f"{self} is not callable")

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.data}>"

# --- Builtins ---

class Builtin(Obj):
    def __init__(self, fn, mem:memory.Memory=None):
        super().__init__(fn, mem)

    def call(self, args, mem):
        return self.data(args, mem)

# --- Primitive types ---

class Num(Obj):
    def __init__(self, data:int|float, mem:memory.Memory=None):
        super().__init__(data, mem)
        # Add arithmetic methods
        self.local.set("add", Builtin(lambda args, m: Num(self.getValue() + args[0].getValue(), m), mem))
        self.local.set("sub", Builtin(lambda args, m: Num(self.getValue() - args[0].getValue(), m), mem))
        self.local.set("mul", Builtin(lambda args, m: Num(self.getValue() * args[0].getValue(), m), mem))
        self.local.set("true_div", Builtin(lambda args, m: Num(self.getValue() / args[0].getValue(), m), mem))
        self.local.set("floor_div", Builtin(lambda args, m: Num(self.getValue() // args[0].getValue(), m), mem))

    def getValue(self):
        val = self.data
        return int(val) if isinstance(val, float) and val.is_integer() else val

class Array(Obj):
    def __init__(self, data:typing.Iterable, mem:memory.Memory=None):
        super().__init__(list(data), mem)

    def call(self, args:list, mem:memory.Memory):
        idx = args[0].getValue()
        if len(args) == 1:
            return self.data[idx]
        elif len(args) == 2:
            return self.data[idx:args[1].getValue()]
        else:
            raise TypeError("Array call expects 1 or 2 arguments")

class String(Array):
    def __init__(self, data:str, mem:memory.Memory=None):
        super().__init__(data, mem)

class Boolean(Obj):
    def __init__(self, data:bool, mem:memory.Memory=None):
        super().__init__(data, mem)


# AST
class Node:
    def eval(self, mem:memory.Memory) -> Obj:
        raise NotImplementedError

class Var(Node):
    def __init__(self, type:str, name:str, value:Node):
        self.type = type
        self.name = name
        self.value = value

    def eval(self, mem:memory.Memory):
        val = self.value.eval(mem)
        mem.set(self.name, val)
        return val
    
    def __repr__(self):
        return f"<Var name:{self.name} value:{self.value}>"

class Call(Node):
    def __init__(self, object:Node, parameter:Node):
        self.object = object
        self.parameter = parameter
    
    def eval(self, mem):
        return self.object.eval(mem).call(self.parameter.eval(mem).getValue())

    def __repr__(self):
        return f"<Call {repr(self.object)}({repr(self.parameter)})>"

class Literal(Node):
    def __init__(self, type:typing.Literal["string","number","boolean","array"], value):
        self.type = type.lower()
        self.value = value

    def eval(self, mem:memory.Memory):
        if self.type == "string":
            return String(self.value, mem)
        elif self.type == "number":
            return Num(self.value, mem)
        elif self.type == "boolean":
            return Boolean(self.value, mem)
        elif self.type == "array":
            return Array(self.value, mem)
        else:
            raise TypeError(f"Unknown literal type {self.type}")
    
    def __repr__(self):
        return f"<Literal of {self.type.capitalize()}: {repr(self.value)}>"

class Identifier(Node):
    def __init__(self, name:str):
        self.name = name

    def eval(self, mem:memory.Memory):
        return mem.get(self.name)

    def __repr__(self):
        return f"<Identifier {self.name}>"
