from __future__ import annotations
from utils import Utils

class Memory:
    def __init__(self, parent:Memory=None):
        self.utils = Utils(self)
        self.vars = {}

        self.parent = parent  # for nested scopes, optional

    def get(self, name: str):
        if name in self.vars:
            return self.vars[name]
        if self.parent:
            return self.parent.get(name)
        raise NameError(f"'{name}' is not defined")

    def set(self, name: str, value):
        import type
        if not isinstance(value,type.obj):
            value = self.utils.pytype_to_ash_type(value)
        self.vars[name] = value

    def exists(self, name: str) -> bool:
        return name in self.vars or (self.parent and self.parent.exists(name))