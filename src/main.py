from frontend.myParser import Parser
from runtime.interpreter import evaluate

def repl():
    parser = Parser
    print("Repl v0.0.1")
    while(True):
        print(">>> ",end='')
        x = ""
        x = input()
        if(x == "exit"):
            break
        program = parser.produceAST(parser, x)
        #print(program)
        
        result = evaluate(program)
        print(result)
    
repl()
