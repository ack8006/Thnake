import copy

class Scope():
    def __init__(self):
        self.variables = {}

    def get(self, var):
        if var in self.variables:
            return copy.deepcopy(self.variables[var])
        else:
            return None

    def add(self, key, val):
        self.variables[key] = val

    def pop(self, key):
        self.variables.pop(key)

