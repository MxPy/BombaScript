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
    AssigmentExpr = "AssigmentExpr"

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
    