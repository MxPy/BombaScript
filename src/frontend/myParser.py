from frontend.myAst import NumericLiteral, Identrifier, BinaryExpr, Expr, Program, Stmt, VarDeclaration, AssigmentExpr
from frontend.myLexer import tokenize, Token, TokenType


class Parser:
    tokens = []
    
    def at(self):
        return self.tokens[0]
    def eat(self):
        return self.tokens.pop(0)
    def expect(self, typeOf: TokenType, err: str):
        prev = self.tokens.pop(0)
        if(prev == None or prev.typeOf != typeOf):
            raise ValueError(f"Parser error: {err} expected: {typeOf} found: {prev}")
        return prev

    def not_eof(self) -> bool:
        return self.tokens[0].typeOf != TokenType.EOF
    def produceAST (self, sourceCode: str) -> Program:
        self.tokens = tokenize(sourceCode)
        program = Program(
            kind= "Program",
            body= []
        )
        while (self.not_eof(self)):
            program.body.append(self.parse_stmt(self))
        return program
    
    def parse_variable_declaration(self) -> Stmt:
        isConstant = True if self.eat(self).typeOf == TokenType.Const else False
        ident = self.expect(self, TokenType.Identifier, "Expected identifier name fallowing keyword let|const").value
        if(self.at(self).typeOf == TokenType.Semicolon):
            self.eat(self)
            if(isConstant):
                raise ValueError("Must assign value to const expr")
            return VarDeclaration(kind = "VarDeclaration", identifier= ident, const = False)
        self.expect(self, TokenType.Equals, "Expected equals token following identifier in variable declaration")
        declaration = VarDeclaration(kind = "VarDeclaration", identifier= ident, const = isConstant, value= self.parse_expr(self))
        self.expect(self, TokenType.Semicolon, "Expected semicolon token following variable declaration")
        return declaration
    
    def parse_stmt(self) -> Stmt:
        if(self.at(self).typeOf == TokenType.Let or self.at(self).typeOf == TokenType.Const):
            return self.parse_variable_declaration(self)
        else:
            return self.parse_expr(self)
    
    
    def parse_expr(self) -> Expr:
        return self.parse_assigment_expr(self)
    
    def parse_assigment_expr(self):
        left = self.parse_addative_expr(self)
        if(self.at(self).typeOf == TokenType.Equals):
            self.eat(self)
            val = self.parse_assigment_expr(self)
            return AssigmentExpr(kind="AssigmentExpr", assigne=left, value= val)
        return left
    
    def parse_addative_expr(self) -> Expr:
        leftt = self.parse_multiplicative_expr(self)
        while(self.at(self).value == "+" or self.at(self).value == "-"):
            #TODO change eat to expect
            operatorr = self.eat(self).value
            rightt = self.parse_multiplicative_expr(self)
            leftt = BinaryExpr(kind="BinaryExpr", left = leftt, right = rightt, operator = operatorr)
        return leftt
    
    def parse_multiplicative_expr(self) -> Expr:
        leftt = self.parse_primary_expr(self)
        while(self.at(self).value == "/" or self.at(self).value == "*" or self.at(self).value == "%"):
            #TODO change eat to expect
            operatorr = self.eat(self).value
            rightt = self.parse_primary_expr(self)
            leftt = BinaryExpr(kind="BinaryExpr", left = leftt, right = rightt, operator = operatorr)
        return leftt
    
    def parse_primary_expr(self) -> Expr:
        tk = self.at(self).typeOf
        if(tk == TokenType.Identifier):
            return Identrifier(kind = "Identifier", symbol=self.eat(self).value)
        elif(tk == TokenType.Number):
            return NumericLiteral(kind = "NumericLiteral", value=float(self.eat(self).value))
        elif (tk == TokenType.OpenParen):
            self.eat(self)
            val = self.parse_expr(self)
            self.expect(self, TokenType.CloseParen, "Close Paren Error")
            return val
        else:
            print(f"unexpected token found during parsing {self.at(self)}")
            self.eat(self)
            
            


