from frontend.myParser import Parser
from runtime.myInterpreter import evaluate
from runtime.myEnvironment import Environment

def bomba():
    parser = Parser
    env = Environment()
    
    
    print("bomba v0.0.2")
    #while(True):
       # print(">>> ",end='')
       # x = ""
       # x = input()
       # if(x == "exit"):
       #     break
       # program = parser.produceAST(parser, x)
        #print(program)
        
      #  result = evaluate(program, env)
      #  print(result)
    with open('src/testFiles/test.txt', 'r') as file:
        data = file.read()
        program = parser.produceAST(parser, data)
        #print(program)
        result = evaluate(program, env)
        #print(result)
    
bomba()
