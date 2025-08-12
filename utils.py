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

    def dump_mem(self,mem):
        for idx, (name, value) in enumerate(mem.vars.items()):
            print(f"{idx} {name}: {str(type(value))[13:-2]} < {value.ref()} >")