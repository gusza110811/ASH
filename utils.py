from __future__ import annotations
import typing

class Utils:
    def __init__(self,memory):
        self.memory = memory
        return

    def can_num(self,string:str):
        try:
            float(string)
            return True
        except:
            return False

    def pytype_to_ash_type(self,value):
        from type import obj,num,string,array
        if isinstance(value,obj):
            return value

        if self.can_num(value):
            return num(value,self.memory)
        if isinstance(value,str):
            return string(value,self.memory)
        if isinstance(value,typing.Iterable):
            return array(value, self.memory)
    
    def ash_type_to_pytype(self,value):
        return value.ref()

    def dump_mem(self,mem:memory.Memory, indent=0):
        for idx, (name, value) in enumerate(mem.vars.items()):
            print(f"{" "*indent}{idx} {name}: {str(type(value))[13:-2]} < {value.ref()} >")
            if value.local:
                self.dump_mem(value.local,indent+4)

if typing.TYPE_CHECKING:
    import type
    import memory
