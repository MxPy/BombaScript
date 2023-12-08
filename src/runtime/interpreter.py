from runtime.values import RuntimeVal, ValueType, NumberVal, NullVal
from frontend.myAst import NodeType, Stmt, NumericLiteral, BinaryExpr, Program

def evaluate_binary_expr(binop: BinaryExpr) -> RuntimeVal:
    leftSide = evaluate(binop.left)
    rightSide = evaluate(binop.right)
    
    if(leftSide.typeOf == "number" and rightSide.typeOf == "number"):
        return evaluate_numeric_binary_expr(leftSide, rightSide, binop.operator)

def evaluate_numeric_binary_expr(leftSide: NumberVal, rightSide: NumberVal, operator: str) -> NumberVal:
    res = 0
    if(operator == "+"):
        res = leftSide.value + rightSide.value
    elif(operator == "-"):
        res = leftSide.value - rightSide.value
    elif(operator == "/"):
        #TODO 0 checks
        res = leftSide.value / rightSide.value
    elif(operator == "*"):
        res = leftSide.value * rightSide.value
    else:
        res = leftSide.value % rightSide.value
    
    return NumberVal(typeOf="number", value=res)
def evaluate_program(program: Program) -> RuntimeVal:
    lastEvald = NullVal(typeOf= "null", value= "null")
    for statement in program.body:
        lastEvald = evaluate(statement)
    return lastEvald

def evaluate(astNode: Stmt) -> RuntimeVal:
    if(astNode.kind == "NumericLiteral"): 
        return NumberVal(typeOf = "number", value = astNode.value)
    elif(astNode.kind == "NullLiteral"): 
        return NullVal(typeOf= "null", value= "null")
    elif(astNode.kind == "Identifier"): 
        pass
    elif(astNode.kind == "BinaryExpr"): 
        return evaluate_binary_expr(astNode)
    elif(astNode.kind == "Program"): 
        return evaluate_program(astNode)
    else:
        print("Not set up AST node")
        