from frontend.myParser import Parser
from runtime.myInterpreter import evaluate
from runtime.myEnvironment import Environment

def repl():
    parser = Parser
    env = Environment
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
