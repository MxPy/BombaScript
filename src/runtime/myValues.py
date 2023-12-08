from dataclasses import dataclass

@dataclass
class ValueType:
    null = "null"
    number = "number"
    boolean = "boolean"


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
    
#macros
def MK_NUM(val: float or int) -> NumberVal:
    return NumberVal(typeOf="number", value= val)

#macros
def MK_BOOL(val: bool = True) -> BooleanVal:
    return BooleanVal(typeOf="boolean", value= val)

#macros
def MK_NULL() -> NullVal:
    return NullVal(typeOf="null", value= "null")