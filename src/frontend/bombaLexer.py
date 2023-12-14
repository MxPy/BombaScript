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
    "while": TokenType.While,
    "=": TokenType.Equals,
    "(": TokenType.OpenParen,
    ")": TokenType.CloseParen,
    ";": TokenType.Semicolon,
    ":": TokenType.Colon,
    "{": TokenType.OpenBrace,
    "}": TokenType.CloseBrace,
    "[": TokenType.OpenBracket,
    "]": TokenType.CloseBracket,
    ".": TokenType.Dot,
    '"': TokenType.Quotation,
    "*": TokenType.BinaryOperator,
    "/": TokenType.BinaryOperator,
    "-": TokenType.BinaryOperator,
    "+": TokenType.BinaryOperator,
    "==": TokenType.BinaryOperator,
    ">=": TokenType.BinaryOperator,
    "<=": TokenType.BinaryOperator,
    ">": TokenType.BinaryOperator,
    "<": TokenType.BinaryOperator,
    
}
BOMBAMAPPER = {
    "TEMPY_CHUJU": "let",
    "DONNA_MAMMA_ES_CHUJOCZITA": "const",
    "NAZWYAM_SIE_CEZARY_BARYKA_I_OD_DWUDZIESTU_MINUT_JESTEM_WLASCICIELEM_TEGO_OTO_SZKLANEGO_DOMU": "fn",
    "SPOJRZ_W_DUPE": "if",
    "TY_TO_CHYBA_LUBISZ": "while",
    "NAPIERDALAC": "=",
    "KIM_JESTES": "(",
    "NAZYWAM_SIE_PAPA_SLON_ALE_WSZYSCY_MOWIA_MI_MARIUSZ": ")",
    "DUPA_GOWNO_CHUJ": ";",
    "KURWA": ",",
    "ARABSKIE_GOGLE": ":",
    "CO_GOTUJESZ": "{",
    "SOLNIK": "}",
    "CZY_ZNACIE_LEGENDE_O_NIEMYM_MICHALKU_KTORY_TAK_ZUL_GUME_ZE_AZ_OSLEPL": "[",
    "KONIEC": "]",
    "ANI_KROKU_DALEJ_KUTAFONY_BO_TA_CIECIWA_ZASPIEWA_TANGO": ".",
    "HIPNOZA": '"',
    "CZTERY_RAZY_WODA_CZTERY_RAZY_PODWOJNIE": "*",
    "KUTARATE_LAMANE_NA_HUDO": '/',
    "JUDASZU_TRAFILES_W_PORTFEL_STRACILEM_MAJATEK": '-',
    "MARIK_RAZ_DWA_TRZY_CZTERY_WROCILEM_ZKOLEGAMI": '+',
    "SREDNIA_HAWAJSKA_DLA_KAZDEGO": '==',
    "O_KURWA_DIABEL": '>=',
    "MYSLALEM_ZE_JESTES_UPOSLEDZONY": '<=',
    "ZA_WYSOKIE_PROGI": '>',
    "MAKAO": '<',
    
}
    
def isInt(value: str) -> bool:
    if value[0] in ('-', '+'):
        return value[1:].isdigit()
    return value.isdigit()

def isSkippable(value: str) -> bool:
    return (value == " " or value == "\n" or value == "\t")

def isAlphabe(value: str) -> bool:
    
    return (value.isalpha() or value == "_")
    
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
        elif(src[0] == "+" or src[0] == "-" or src[0] == "*" or src[0] == "/" or src[0] == "%" or src[0] == ">" or src[0] == "<"):
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
            elif(isAlphabe(src[0])):
                ident = ""
                while(len(src)>0 and isAlphabe(src[0])):
                    ident += src.pop(0)
                if(ident in BOMBAMAPPER):
                    tokens.append(getToken(BOMBAMAPPER[ident], KEYWORDS[BOMBAMAPPER[ident]]))
                else:
                    tokens.append(getToken(ident, TokenType.Identifier))
            elif(isSkippable(src[0])):
                src.pop(0)
            else:
                tokens.append(getToken(src.pop(0), TokenType.Unreconized))
    tokens.append(getToken("EndOfFile", TokenType.EOF))
    return tokens



