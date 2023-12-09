from runtime.myValues import RuntimeVal, ValueType, NumberVal, NullVal
from frontend.myAst import NodeType, Stmt, NumericLiteral, BinaryExpr, Program, Identrifier, VarDeclaration
from runtime.myEnvironment import Environment


def evaluate_program(program: Program, env: Environment) -> RuntimeVal:
    lastEvald = NullVal(typeOf= "null", value= "null")
    for statement in program.body:
        lastEvald = evaluate(statement , env)
    return lastEvald
