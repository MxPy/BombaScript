from runtime.myValues import RuntimeVal, ValueType, NumberVal, NullVal


class Environment:
    parent: 'Environment' = None
    variables: dict = {}
    constVariables: list = []
    
    def __init__(self, parentENV: 'Environment' = None) -> None:
        self.parent = parentENV
        self.variables = {}
        self.constVariables = []

    def declareVar(self, varName: str, value: RuntimeVal, isConstant: bool = False) -> RuntimeVal:
        if varName in self.variables.keys():
            raise NameError("Varibale already declared")
        if(isConstant):
            self.constVariables.append(varName)
        self.variables.update({varName: value}) 
        return value
    
    def assignVar(self, varName: str, value: RuntimeVal) -> RuntimeVal:
        env = self.resolve(varName)
        if(varName in env.constVariables):
            raise ValueError("Cannot assign value to const variable")
        env.variables.update({varName: value})
        return value 
        
    def resolve(self, varName: str) -> 'Environment':
        if varName in self.variables.keys():
            return self
        if self.parent == None:
            raise NameError(f"Cannot resolve {varName} as is not exist in current scope")
        return self.parent.resolve(varName)
    
    def lookupVar(self, varName: str) -> RuntimeVal:
        env = self.resolve(varName)
        return env.variables.get(varName)