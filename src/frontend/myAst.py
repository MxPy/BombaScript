from dataclasses import dataclass


@dataclass
class NodeType:
    #STMT
    Program = "Program"
    VarDeclaration = "VarDeclaration"
    FunctionDeclaration = "FunctionDeclaration"
    IfStmtDeclaration = "IfStmtDeclaration"
    WhlieLoopDeclaration = "WhlieLoopDeclaration"
    
    #EXPR
    NumericLiteral = "NumericLiteral"
    StringLiteral = "StringLiteral" #todo fix whitespaces
    Identifier = "Identifier"
    BinaryExpr = "BinaryExpr"
    MemberExpr = "MemberExpr"
    CallExpr = "CallExpr"
    AssigmentExpr = "AssigmentExpr"
    Property = "Property"
    ObjectLiteral = "ObjectLiteral"
    ListLiteral = "ListLiteral"

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
class FunctionDeclaration(Stmt):
    kind = NodeType.FunctionDeclaration
    params: list[str]
    name: str
    body: Stmt

@dataclass
class IfStmtDeclaration(Stmt):
    kind = NodeType.IfStmtDeclaration
    key: Expr
    body: Stmt

@dataclass
class WhlieLoopDeclaration(Stmt):
    kind = NodeType.WhlieLoopDeclaration
    key: Expr
    body: Stmt

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
    kind = NodeType.NumericLiteral
    value: int or float
    
@dataclass
class StringLiteral(Expr):
    kind = NodeType.StringLiteral
    value: str

@dataclass
class Property(Expr):
    kind = NodeType.Property
    key: str
    value: Expr = None
    
@dataclass
class ObjectLiteral(Expr):
    kind = NodeType.ObjectLiteral
    properties: list[Property]
    
@dataclass
class ListLiteral(Expr):
    kind = NodeType.ListLiteral
    properties: list