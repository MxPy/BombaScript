from enum import Enum
from dataclasses import dataclass

class TokenType(Enum):
    #Literal Types
    Number = 0
    Identifier = 1

    #Keywords
    Let = 2

    #Grouping * Operators
    BinaryOperator = 3
    Equals = 4
    OpenParen = 5
    CloseParen = 6

KEYWORDS = {
    "let": TokenType.Let
}
    
def isInt(value: str) -> bool:
    if value[0] in ('-', '+'):
        return value[1:].isdigit()
    return value.isdigit()

def isSkippable(value: str) -> bool:
    return (value == " " or value == "\n" or value == "\t")

    
def getToken(value: str, typeOf: TokenType):
    return {"value": value, "type": typeOf.value}
    
def tokenize(sourceCode: str) -> list:
    tokens = []
    src = list(sourceCode)
    
    while(len(src)>0):
        
        if(src[0] == "("):
            tokens.append(getToken(src.pop(0), TokenType.OpenParen))
        elif(src[0] == ")"):
            tokens.append(getToken(src.pop(0), TokenType.CloseParen))
        elif(src[0] == "+" or src[0] == "-" or src[0] == "*" or src[0] == "/"):
            tokens.append(getToken(src.pop(0), TokenType.BinaryOperator))
        elif(src[0] == "="):
            tokens.append(getToken(src.pop(0), TokenType.Equals))
        else:
            if(isInt(src[0])):
                num = ""
                while(len(src)>0 and isInt(src[0])):
                    num += src.pop(0)
                tokens.append(getToken(num, TokenType.Number))
            elif(src[0].isalpha()):
                ident = ""
                while(len(src)>0 and src[0].isalpha()):
                    ident += src.pop(0)
                if(ident in KEYWORDS):
                    tokens.append(getToken(ident, KEYWORDS[ident]))
                else:
                    tokens.append(getToken(ident, TokenType.Identifier))
            elif(isSkippable(src[0])):
                src.pop(0)
            else:
                print(f"unreconized char found {src[0]}")
                break
    return tokens


with open("testFiles/test.txt", "r") as f:
    for line in f.readlines():
        print(tokenize(line))