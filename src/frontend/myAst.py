from dataclasses import dataclass


@dataclass
class NodeType:
    #STMT
    Program = "Program"
    VarDeclaration = "VarDeclaration"
    
    #EXPR
    NumericLiteral = "NumericLiteral"
    Identifier = "Identifier"
    BinaryExpr = "BinaryExpr"
    MemberExpr = "MemberExpr"
    CallExpr = "CallExpr"
    AssigmentExpr = "AssigmentExpr"
    Property = "Property"
    ObjectLiteral = "ObjectLiteral"

@dataclass
class Stmt:
    kind: NodeType

@dataclass
class Expr(Stmt):
    pass
    
@dataclass
class Program(Stmt):
    kind = NodeType.Program
    body: list[Stmt]
    

@dataclass
class VarDeclaration(Stmt):
    kind = NodeType.VarDeclaration
    const: bool
    identifier: str
    value: Expr = None

@dataclass
class BinaryExpr(Expr):
    kind = NodeType.BinaryExpr
    left: Expr
    right: Expr
    operator: str

@dataclass
class CallExpr(Expr):
    kind = NodeType.CallExpr
    args: list[Expr]
    clle: Expr
    
@dataclass
class MemberExpr(Expr):
    kind = NodeType.MemberExpr
    obj: Expr
    prop: Expr
    computed: bool

@dataclass
class AssigmentExpr(Expr):
    kind = NodeType.AssigmentExpr
    assigne: Expr
    value: Expr
    
@dataclass
class Identrifier(Expr):
    kind = NodeType.Identifier
    symbol: str
    
@dataclass
class NumericLiteral(Expr):
    kind = NodeType.Identifier
    value: int or float

@dataclass
class Property(Expr):
    kind = NodeType.Property
    key: str
    value: Expr = None
    
@dataclass
class ObjectLiteral(Expr):
    kind = NodeType.ObjectLiteral
    properties: list[Property]