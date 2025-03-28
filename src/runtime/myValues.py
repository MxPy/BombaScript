from dataclasses import dataclass
from src.frontend.myAst import Stmt

@dataclass
class ValueType:
    null = "null"
    number = "number"
    string = "string"
    boolean = "boolean"
    obj = "obj"
    native_fn = "native_fn"
    function = "function"
    lsit = "lsit"


@dataclass
class RuntimeVal:
    typeOf: ValueType
    
@dataclass
class NullVal(RuntimeVal):
    typeOf: ValueType.null
    value: str

@dataclass
class BooleanVal(RuntimeVal):
    typeOf: ValueType.boolean
    value: bool
    
@dataclass
class NumberVal(RuntimeVal):
    typeOf: ValueType.number
    value: float or int
    
@dataclass
class StringVal(RuntimeVal):
    typeOf: ValueType.string
    value: str
    
@dataclass
class ObjectVal(RuntimeVal):
    typeOf: ValueType.obj
    properties: dict
    
@dataclass
class ListVal(RuntimeVal):
    typeOf: ValueType.lsit
    properties: list
    

def FunctionCall (args: list[RuntimeVal], env) -> RuntimeVal:
    return MK_NULL()

@dataclass
class NativeFnVal(RuntimeVal):
    typeOf: ValueType.native_fn
    call: FunctionCall
    
#TODO resolve importing problems with Enviroment
@dataclass
class FunctionVal(RuntimeVal):
    typeOf: ValueType.function
    name: str
    params: list[str]
    declarationEnv: 'Enviroment'
    body: list[Stmt]

#macros
def MK_NUM(val: float or int) -> NumberVal:
    return NumberVal(typeOf="number", value= val)


#macros
def MK_BOOL(val: bool = True) -> BooleanVal:
    return BooleanVal(typeOf="boolean", value= val)

#macros
def MK_NULL() -> NullVal:
    return NullVal(typeOf="null", value= None)

#macros
def MK_NATIVE_FN(calle: FunctionCall) -> NullVal:
    return NativeFnVal(typeOf="native_fn", call= calle)
