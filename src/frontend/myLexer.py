from enum import Enum
from dataclasses import dataclass


class TokenType(Enum):
    #Literal Types
    Number = 0
    Identifier = 1

    #Keywords
    Let = 2
    Const = 8
    Fn = 17 
    IF = 20
    While = 21

    #Grouping * Operators
    BinaryOperator = 3
    Equals = 4 #=
    OpenParen = 5 #(
    CloseParen = 6  #)
    EOF = 7
    Semicolon = 9 #;
    Comma = 10 #,
    Colon = 11  #:
    OpenBrace = 12 #{
    CloseBrace = 13 #}
    OpenBracket = 14 #[
    CloseBracket = 15 #]
    Dot = 16 #.
    Quotation = 18 #"
    Unreconized = 19
    
    
@dataclass
class Token():
    value: str
    typeOf: TokenType

KEYWORDS = {
    "let": TokenType.Let,
    "const": TokenType.Const,
    "fn": TokenType.Fn,
    "if": TokenType.IF,
    "while": TokenType.While
}
    
def isInt(value: str) -> bool:
    if value[0] in ('-', '+'):
        return value[1:].isdigit()
    return value.isdigit()

def isSkippable(value: str) -> bool:
    return (value == " " or value == "\n" or value == "\t")

    
def getToken(value: str, typeOf: TokenType) -> Token:
    return Token(value, typeOf)
def checkIndex(i, list):
    try:
        return list[i]
    except IndexError:
        return False   
def tokenize(sourceCode: str) -> list:
    tokens = []
    src = list(sourceCode)
    
    while(len(src)>0):
        
        if(src[0] == "("):
            tokens.append(getToken(src.pop(0), TokenType.OpenParen))
        elif(src[0] == ")"):
            tokens.append(getToken(src.pop(0), TokenType.CloseParen))
        elif(src[0] == "{"):
            tokens.append(getToken(src.pop(0), TokenType.OpenBrace))
        elif(src[0] == "}"):
            tokens.append(getToken(src.pop(0), TokenType.CloseBrace))
        elif(src[0] == "["):
            tokens.append(getToken(src.pop(0), TokenType.OpenBracket))
        elif(src[0] == "]"):
            tokens.append(getToken(src.pop(0), TokenType.CloseBracket))
        elif(checkIndex(1, src) and (src[0]+src[1] == "==" or src[0]+src[1] == ">=" or src[0]+src[1] == "<=")):
            tokens.append(getToken(src.pop(0)+src.pop(0), TokenType.BinaryOperator))
        elif(src[0] == "+" or src[0] == "-" or src[0] == "*" or src[0] == "/" or src[0] == "%"   or src[0] == ">" or src[0] == "<"):
            tokens.append(getToken(src.pop(0), TokenType.BinaryOperator))
        elif(src[0] == "="):
            tokens.append(getToken(src.pop(0), TokenType.Equals))
        elif(src[0] == ";"):
            tokens.append(getToken(src.pop(0), TokenType.Semicolon))
        elif(src[0] == ":"):
            tokens.append(getToken(src.pop(0), TokenType.Colon))
        elif(src[0] == ","):
            tokens.append(getToken(src.pop(0), TokenType.Comma))
        elif(src[0] == "."):
            tokens.append(getToken(src.pop(0), TokenType.Dot))
        elif(src[0] == '"'):
            tokens.append(getToken(src.pop(0), TokenType.Quotation))
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
                tokens.append(getToken(src.pop(0), TokenType.Unreconized))
    tokens.append(getToken("EndOfFile", TokenType.EOF))
    return tokens



