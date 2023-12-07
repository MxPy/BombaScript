from frontend.myParser import Parser

def repl():
    parser = Parser
    print("Repl v0.0.1")
    while(True):
        print(">>>",end='')
        x = ""
        x = input()
        if(x == "exit"):
            break
        program = parser.produceAST(parser, x)
        print(program)
    
repl()
