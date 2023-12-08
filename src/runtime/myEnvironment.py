from runtime.myValues import RuntimeVal, ValueType, NumberVal, NullVal


class Environment:
    parent: 'Environment'
    variables: dict = {}
    
    def __init__(self, parentENV: 'Environment') -> None:
        self.parent = parentENV
        self.variables = {}

    def declareVar(self, varName: str, value: RuntimeVal) -> RuntimeVal:
        if varName in self.variables.keys():
            raise NameError("Varibale already declared")
        
        self.variables.update({varName: value}) 
        return value
    
    def assignVar(self, varName: str, value: RuntimeVal) -> RuntimeVal:
        env = self.resolve(self, varName)
        env.variables.update({varName: value})
        return value 
        
    def resolve(self, varName: str) -> 'Environment':
        if varName in self.variables.keys():
            return self
        if self.parent == None:
            raise NameError(f"Cannot resolve {varName} as is not exist in current scope")
        return self.parent.resolve(self.parent, varName)
    
    def lookupVar(self, varName: str) -> RuntimeVal:
        env = self.resolve(self, varName)
        return env.variables.get(varName)