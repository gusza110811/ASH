from __future__ import annotations
import typing

class Utils:
    def __init__(self):
        return

    def can_num(self,string:str):
        try:
            float(string)
            return True
        except:
            return False

    def dump_mem(self,mem:memory.Memory, indent=0):
        for idx, (key, value) in enumerate(mem.vars.items()):
            if not isinstance(key, str): continue
            print(f"{" "*indent}{idx} {key}: {str(type(value))[13:-2]} < {value.ref()} >")
            if value.local:
                self.dump_mem(value.local,indent+4)

if typing.TYPE_CHECKING:
    import type
    import memory
