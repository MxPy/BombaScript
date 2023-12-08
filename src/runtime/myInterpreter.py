from runtime.myValues import RuntimeVal, ValueType, NumberVal, NullVal, MK_NULL
from frontend.myAst import NodeType, Stmt, NumericLiteral, BinaryExpr, Program, Identrifier, VarDeclaration, AssigmentExpr
from runtime.myEnvironment import Environment

def evaluate_binary_expr(binop: BinaryExpr, env: Environment) -> RuntimeVal:
    leftSide = evaluate(binop.left, env)
    rightSide = evaluate(binop.right, env)
    
    if(leftSide.typeOf == "number" and rightSide.typeOf == "number"):
        return evaluate_numeric_binary_expr(leftSide, rightSide, binop.operator)
    return NullVal(typeOf= "null", value= "null")

def evaluate_numeric_binary_expr(leftSide: NumberVal, rightSide: NumberVal, operator: str) -> NumberVal:
    res = 0
    if(operator == "+"):
        res = leftSide.value + rightSide.value
    elif(operator == "-"):
        res = leftSide.value - rightSide.value
    elif(operator == "/"):
        if(rightSide.value == 0):
            raise ValueError("Dividing by 0 is not allowed")
        res = leftSide.value / rightSide.value
    elif(operator == "*"):
        res = leftSide.value * rightSide.value
    else:
        res = leftSide.value % rightSide.value
    
    return NumberVal(typeOf="number", value=res)

def evaluate_program(program: Program, env: Environment) -> RuntimeVal:
    lastEvald = NullVal(typeOf= "null", value= "null")
    for statement in program.body:
        lastEvald = evaluate(statement , env)
    return lastEvald

def evaluate_var_declaration(varDeclaration: VarDeclaration, env: Environment) -> RuntimeVal:
    val=evaluate(varDeclaration.value, env) if varDeclaration.value else MK_NULL()
    return env.declareVar(env, varName=varDeclaration.identifier,value=val,isConstant= varDeclaration.const)

def evaluate_identifier(ident: Identrifier, env: Environment) -> RuntimeVal:
    val = env.lookupVar(env, ident.symbol)
    return val

def evaluate_assignment(node: AssigmentExpr, env: Environment) -> RuntimeVal:
    if(node.assigne.kind != "Identifier"):
        raise  ValueError("Invalid LHS identifier")
    val = env.assignVar(env, varName= node.assigne.symbol, value= evaluate(node.value, env))
    return val

def evaluate(astNode: Stmt, env: Environment) -> RuntimeVal:
    if(astNode.kind == "NumericLiteral"): 
        return NumberVal(typeOf = "number", value = astNode.value)
    elif(astNode.kind == "Identifier"): 
       return evaluate_identifier(astNode ,env)
    elif(astNode.kind == "BinaryExpr"): 
        return evaluate_binary_expr(astNode, env)
    elif(astNode.kind == "Program"): 
        return evaluate_program(astNode, env)
    elif(astNode.kind == "VarDeclaration"): 
        return evaluate_var_declaration(astNode, env)
    elif(astNode.kind == "AssigmentExpr"): 
        return evaluate_assignment(astNode, env)
    else:
        raise ValueError("Not set up AST node")
        