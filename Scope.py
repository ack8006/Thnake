class Scope():
    def __init__(self):
        self.variables = {}
        self.methods = {}

    def get(self, var):
        if var in self.variables:
            return self.variables[var]
        else:
            return None

    def add(self, key, val):
        self.variables[key] = val

    def getMethod(self, meth):
        if meth in self.methods:
            return self.methods[meth]
        else:
            return None

    def addMethod(self, key, val):
        self.methods[key] = val

