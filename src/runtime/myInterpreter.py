from src.runtime.myValues import RuntimeVal, ValueType, NumberVal, NullVal, ObjectVal, MK_NULL, NativeFnVal, FunctionVal, StringVal, ListVal
from src.frontend.myAst import NodeType, Stmt, NumericLiteral, BinaryExpr, Program, Identrifier, VarDeclaration, AssigmentExpr, ObjectLiteral, Property, CallExpr, MemberExpr, FunctionDeclaration, StringLiteral, IfStmtDeclaration, WhlieLoopDeclaration, ListLiteral

from src.runtime.myEnvironment import Environment

def evaluate_binary_expr(binop: BinaryExpr, env: Environment) -> RuntimeVal:
    leftSide = evaluate(binop.left, env)
    rightSide = evaluate(binop.right, env)
    
    if(leftSide.typeOf == "number" and rightSide.typeOf == "number"):
        return evaluate_numeric_binary_expr(leftSide, rightSide, binop.operator, env)
    return NullVal(typeOf= "null", value= "null")

def evaluate_numeric_binary_expr(leftSide: NumberVal, rightSide: NumberVal, operator: str,  env: Environment):
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
    elif(operator == "=="):
        return env.lookupVar("true") if leftSide.value == rightSide.value else env.lookupVar("false")
    elif(operator == ">="):
        return env.lookupVar("true") if leftSide.value >= rightSide.value else env.lookupVar("false") 
    elif(operator == "<="):
        return env.lookupVar("true") if leftSide.value <= rightSide.value else env.lookupVar("false")
    elif(operator == ">"):
        return env.lookupVar("true") if leftSide.value > rightSide.value else env.lookupVar("false")
    elif(operator == "<"):
        return env.lookupVar("true") if leftSide.value < rightSide.value else env.lookupVar("false")
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
    return env.declareVar(varName=varDeclaration.identifier,value=val,isConstant= varDeclaration.const)

def evaluate_identifier(ident: Identrifier, env: Environment) -> RuntimeVal:
    val = env.lookupVar(ident.symbol)
    return val

def evaluate_assignment(node: AssigmentExpr, env: Environment) -> RuntimeVal:
    if(node.assigne.kind == "MemberExpr"):
        obj = evaluate(node.assigne.obj, env)
        try:
            obj.properties[node.assigne.prop.symbol] = evaluate(node.value, env)
            return obj.properties[node.assigne.prop.symbol]
        except AttributeError:
            obj.properties[int(evaluate(node.assigne.prop, env).value)] = evaluate(node.value, env)
            return obj.properties[int(evaluate(node.assigne.prop, env).value)]
        except TypeError:
            obj.properties[int(evaluate(node.assigne.prop, env).value)] = evaluate(node.value, env)
            return obj.properties[int(evaluate(node.assigne.prop, env).value)]
    if(node.assigne.kind != "Identifier"):
        raise  ValueError(f"Invalid LHS identifier {node.assigne}")
    val = env.assignVar(varName= node.assigne.symbol, value= evaluate(node.value, env))
    return val

def evaluate_object_expr(obj: ObjectLiteral, env: Environment) -> RuntimeVal:
    object = ObjectVal( typeOf="obj", properties= {})
    for prop in obj.properties:
        if(prop.value):
            val = evaluate(prop.value, env)
        else:
            val = env.lookupVar(prop.key)
        object.properties[prop.key] = val
    return object

def evaluate_list_expr(obj: ListLiteral, env: Environment) -> RuntimeVal:
    object = ListVal( typeOf="obj", properties= [])
    for prop in obj.properties:
        if(prop):
            val = evaluate(prop, env)
        else:
            val = env.lookupVar(prop.key)
        object.properties.append(val)
    return object

def evaluate_call_expr(expr: CallExpr, env: Environment) -> RuntimeVal:
    args = []
    for arg in expr.args:
        args.append(evaluate(arg, env))
    fn = evaluate(expr.clle, env)
    if(fn.typeOf == "native_fn"):
        result = fn.call(args, env)
        return result
    elif(fn.typeOf == "function"):
        scope = Environment(fn.declarationEnv)
        for count, ele in enumerate(fn.params):
            scope.declareVar(ele, args[count], False)
        result = MK_NULL()
        for st in fn.body:
            result = evaluate(st, scope)
        return result
    raise ValueError(f"Cannot call not a function {fn}")
    

def evaluate_member_expr(expr: MemberExpr, env: Environment) -> RuntimeVal:
    obj = evaluate(expr.obj, env)
    try:
        return obj.properties.get(expr.prop.symbol)
    except AttributeError:
        return obj.properties[int(evaluate(expr.prop, env).value)]

def evaluate_function_declaration(declaration: FunctionDeclaration, env: Environment) -> RuntimeVal:
    fun = FunctionVal(typeOf="function", name= declaration.name, params=declaration.params, declarationEnv=env, body=declaration.body)
    return env.declareVar(declaration.name, fun, True)

def evaluate_if_stmt_declaration(declaration: IfStmtDeclaration, env: Environment) -> RuntimeVal:
    key = evaluate(declaration.key, env)
    scope = Environment(env)
    result = MK_NULL()
    if(key.value):
        for st in declaration.body:
            result = evaluate(st, scope)
        return result
    
def evaluate_while_loop_declaration(declaration: WhlieLoopDeclaration, env: Environment) -> RuntimeVal:
    scope = Environment(env)
    result = MK_NULL()
    while(evaluate(declaration.key, env).value):
        for st in declaration.body:
            result = evaluate(st, scope)
    
    return result
    

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
    elif(astNode.kind == "FunctionDeclaration"):
        return evaluate_function_declaration(astNode, env)
    elif(astNode.kind == "IfStmtDeclaration"):
        return evaluate_if_stmt_declaration(astNode, env)
    elif(astNode.kind == "WhlieLoopDeclaration"):
        return evaluate_while_loop_declaration(astNode, env)
    elif(astNode.kind == "AssigmentExpr"): 
        return evaluate_assignment(astNode, env)
    elif(astNode.kind == "ObjectLiteral"): 
        return evaluate_object_expr(astNode, env)
    elif(astNode.kind == "StringLiteral"): 
        return StringVal(typeOf="string", value=astNode.value)
    elif(astNode.kind == "CallExpr"): 
        return evaluate_call_expr(astNode, env)
    elif(astNode.kind == "ListLiteral"): 
        return evaluate_list_expr(astNode, env)
    elif(astNode.kind == "MemberExpr"): 
        return evaluate_member_expr(astNode, env)
    else:
        raise ValueError(f"Not set up AST node: {astNode}")
        