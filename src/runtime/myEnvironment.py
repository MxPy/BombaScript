from runtime.myValues import RuntimeVal, ValueType, NumberVal, NullVal
from runtime.myValues import MK_NULL, MK_NUM, MK_BOOL, MK_NATIVE_FN
from datetime import datetime

class Environment:
    parent: 'Environment' = None
    variables: dict = {}
    constVariables: list = []
    
    def __init__(self, parentENV: 'Environment' = None) -> None:
        self.parent = parentENV
        self.variables = {}
        self.constVariables = []
        if(parentENV == None):
            self.declare_global_variables()
            self.declare_global_functios()

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
    
    def declare_global_variables(self):
        self.declareVar("true", MK_BOOL(True), True)
        self.declareVar("false", MK_BOOL(False), True)
        self.declareVar("null", MK_NULL(), True)
        
    def print_args(self, args: list):
            for arg in args:
                print(arg.value)
            return MK_NULL()
    
    def declare_global_functios(self):
        self.declareVar("print", MK_NATIVE_FN(lambda args, env: self.print_args(args)), True)
        self.declareVar("time", MK_NATIVE_FN(lambda arg, env: datetime.now()), True)