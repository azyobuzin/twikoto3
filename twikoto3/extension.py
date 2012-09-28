# -*- coding: utf-8 -*-

class Extension:
    def __init__(self, action):
        self.action = action
    
    def __ror__(self, source):
        return self.action(source)

def let(action):
    return Extension(action)

def apply(action):
    def handler(source):
        action(source)
        return source
    
    return Extension(handler)

def noneoremptystr():
    return Extension(lambda str: str is None or str == "")

def none(defaultvalue):
    return Extension(lambda obj: obj if obj is not None else defaultvalue)
