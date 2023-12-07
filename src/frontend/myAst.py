from dataclasses import dataclass

@dataclass
class NodeType:
    Program = "Program"
    NumericLiteral = "NumericLiteral"
    Identifier = "Identifier"
    BinaryExpr = "BinaryExpr"

@dataclass
class Stmt:
    kind: NodeType
    
@dataclass
class Program(Stmt):
    kind = NodeType.Program
    body: list[Stmt]

@dataclass
class Expr(Stmt):
    pass

@dataclass
class BinaryExpr(Expr):
    kind = NodeType.BinaryExpr
    left: Expr
    right: Expr
    operator: str
    
@dataclass
class Identrifier(Expr):
    kind = NodeType.Identifier
    symbol: str
    
@dataclass
class NumericLiteral(Expr):
    kind = NodeType.Identifier
    value: int or float