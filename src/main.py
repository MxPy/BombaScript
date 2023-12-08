from frontend.myParser import Parser
from runtime.myInterpreter import evaluate
from runtime.myEnvironment import Environment
from runtime.myValues import MK_NULL, MK_NUM, MK_BOOL

def repl():
    parser = Parser
    env = Environment
    env.declareVar(env, "x", MK_NUM(100.5))
    env.declareVar(env, "true", MK_BOOL(True))
    env.declareVar(env, "false", MK_BOOL(False))
    env.declareVar(env, "null", MK_NULL())
    print("Repl v0.0.1")
    while(True):
        print(">>> ",end='')
        x = ""
        x = input()
        if(x == "exit"):
            break
        program = parser.produceAST(parser, x)
        #print(program)
        
        result = evaluate(program, env)
        print(result)
    
repl()
