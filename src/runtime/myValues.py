from dataclasses import dataclass

@dataclass
class ValueType:
    null = "null"
    number = "number"


@dataclass
class RuntimeVal:
    typeOf: ValueType
    
@dataclass
class NullVal(RuntimeVal):
    typeOf: ValueType.null
    value: str
    
@dataclass
class NumberVal(RuntimeVal):
    typeOf: ValueType.number
    value: float or int