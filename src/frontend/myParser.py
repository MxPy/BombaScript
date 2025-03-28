from src.frontend.myAst import NumericLiteral, Identrifier, BinaryExpr, Expr, Program, Stmt, VarDeclaration, AssigmentExpr, Property, ObjectLiteral, CallExpr, MemberExpr, FunctionDeclaration, StringLiteral, IfStmtDeclaration, WhlieLoopDeclaration, ListLiteral
#from frontend.myLexer import tokenize, Token, TokenType
from src.frontend.bombaLexer import tokenize, Token, TokenType


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
        #print(program)
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
        elif(self.at(self).typeOf == TokenType.Fn):
            return self.parse_function_declaration(self)
        elif(self.at(self).typeOf == TokenType.IF):
            return self.parse_if_stmt_declaration(self)
        elif(self.at(self).typeOf == TokenType.While):
            return self.parse_while_loop_declaration(self)
        else:
            return self.parse_expr(self)
    
    def parse_function_declaration(self) -> Stmt:
        self.eat(self)
        nae = self.expect(self, TokenType.Identifier, "Expected name of function following Fn keyword").value
        args = self.parse_args(self)
        pars = []
        for arg in args:
            if(arg.kind != "Identifier"):
                raise ValueError(f"Inside function declaration parameters to be string {arg}")
            pars.append(arg.symbol)
        self.expect(self, TokenType.OpenBrace, "Expected body following function declaration")
        bod = []
        while(self.not_eof and self.at(self).typeOf != TokenType.CloseBrace):
            bod.append(self.parse_stmt(self))
        self.expect(self, TokenType.CloseBrace, "Expected closing brace following function body")
        fun = FunctionDeclaration(kind="FunctionDeclaration", name= nae, body=bod, params=pars)
        return fun
    
    def parse_if_stmt_declaration(self) -> Stmt:
        self.eat(self)
        self.expect(self, TokenType.OpenParen, "Expected open paren followig if keyword")
        kay = self.parse_expr(self)
        self.expect(self, TokenType.CloseParen, "Expected close paren followig if expr")
        self.expect(self, TokenType.OpenBrace, "Expected body following if statement")
        bod = []
        while(self.not_eof and self.at(self).typeOf != TokenType.CloseBrace):
            bod.append(self.parse_stmt(self))
        self.expect(self, TokenType.CloseBrace, "Expected closing brace following if body")
        
        fun = IfStmtDeclaration(kind="IfStmtDeclaration", key= kay, body=bod)
        return fun
    
    def parse_while_loop_declaration(self) -> Stmt:
        self.eat(self)
        self.expect(self, TokenType.OpenParen, "Expected open paren followig while keyword")
        kay = self.parse_expr(self)
        self.expect(self, TokenType.CloseParen, "Expected close paren followig while expr")
        self.expect(self, TokenType.OpenBrace, "Expected body following while statement")
        bod = []
        while(self.not_eof and self.at(self).typeOf != TokenType.CloseBrace):
            bod.append(self.parse_stmt(self))
        self.expect(self, TokenType.CloseBrace, "Expected closing brace following while body")
        
        fun = WhlieLoopDeclaration(kind="WhlieLoopDeclaration", key= kay, body=bod)
        return fun
    
    def parse_expr(self) -> Expr:
        return self.parse_assigment_expr(self)
    
    def parse_object_expr(self) -> Expr:
        if(self.at(self).typeOf != TokenType.OpenBrace):
            return self.parse_list_expr(self)
        
        self.expect(self, TokenType.OpenBrace, "something went horribly wrong")
        props = []
        while(self.not_eof(self) and self.at(self).typeOf != TokenType.CloseBrace):
            keyy = self.expect(self, TokenType.Identifier, "Expected object literal key ").value
            if(self.at(self).typeOf == TokenType.Comma):
                self.eat(self)
                props.append(Property(kind="Property", key=keyy))
                continue
            elif(self.at(self).typeOf == TokenType.CloseBrace):
                props.append(Property(kind="Property", key=keyy))
                continue
            
            self.expect(self, TokenType.Colon, "Expected colon after object literal key")
            val = self.parse_expr(self)
            props.append(Property(kind="Property", key=keyy, value=val))
            
            if(self.at(self).typeOf != TokenType.CloseBrace):
                self.expect(self, TokenType.Comma, "Expected comma or closing barce after object property")
        
        self.expect(self, TokenType.CloseBrace, "Expected closing brace after object properties")
        return ObjectLiteral(kind="ObjectLiteral", properties=props)
    
    def parse_list_expr(self) -> Expr:
        if(self.at(self).typeOf != TokenType.OpenBracket):
            return self.parse_comparsion_expr(self)
        
        self.expect(self, TokenType.OpenBracket, "something went horribly wrong")
        props = []
        while(self.not_eof(self) and self.at(self).typeOf != TokenType.CloseBracket):
            val = self.parse_expr(self)
            if(self.at(self).typeOf == TokenType.Comma):
                self.eat(self)
                props.append(val)
                continue
            elif(self.at(self).typeOf == TokenType.CloseBracket):
                props.append(val)
                continue
            if(self.at(self).typeOf != TokenType.CloseBracket):
                self.expect(self, TokenType.Comma, "Expected comma or closing barce after object property")
        
        self.expect(self, TokenType.CloseBracket, "Expected closing brace after object properties")
        return ListLiteral(kind="ListLiteral", properties=props)
    
    def parse_assigment_expr(self):
        left = self.parse_object_expr(self)
        if(self.at(self).typeOf == TokenType.Equals):
            self.eat(self)
            val = self.parse_assigment_expr(self)
            return AssigmentExpr(kind="AssigmentExpr", assigne=left, value= val)
        return left
    
    def parse_comparsion_expr(self) -> Expr:
        leftt = self.parse_addative_expr(self)
        while(self.at(self).value == "==" or self.at(self).value == ">=" or self.at(self).value == "<=" or self.at(self).value == ">" or self.at(self).value == "<"):
            #TODO change eat to expect
            operatorr = self.eat(self).value
            rightt = self.parse_addative_expr(self)
            leftt = BinaryExpr(kind="BinaryExpr", left = leftt, right = rightt, operator = operatorr)
        return leftt
    
    def parse_addative_expr(self) -> Expr:
        leftt = self.parse_multiplicative_expr(self)
        while(self.at(self).value == "+" or self.at(self).value == "-"):
            #TODO change eat to expect
            operatorr = self.eat(self).value
            rightt = self.parse_multiplicative_expr(self)
            leftt = BinaryExpr(kind="BinaryExpr", left = leftt, right = rightt, operator = operatorr)
        return leftt
    
    
    def parse_call_member_expr(self) -> Expr:
        member = self.parse_member_expr(self)
        
        if(self.at(self).typeOf == TokenType.OpenParen):
            return self.parse_call_expr(self, member)
        
        return member
    
    def parse_call_expr(self, caller: Expr) -> Expr:
        call_expr = CallExpr(kind="CallExpr", clle=caller,args=self.parse_args(self))
        
        if(self.at(self).typeOf == TokenType.OpenParen):
            call_expr = self.parse_call_expr(self, call_expr)
            
        return call_expr
    
    def parse_args(self) -> list[Expr]:
        self.expect(self, TokenType.OpenParen, "Expected open paren")
        
        args = [] if self.at(self).typeOf == TokenType.CloseParen else self.parse_call_args_list(self)
        self.expect(self, TokenType.CloseParen, "Expected closed paren after arguments list")
        
        return args
    
    def parse_call_args_list(self) -> list[Expr]:
        args = [self.parse_assigment_expr(self)]
        
        while(self.at(self).typeOf == TokenType.Comma and self.eat(self)):
            args.append(self.parse_assigment_expr(self))
            
        return args
    
    def parse_member_expr(self) -> Expr:
        objc = self.parse_primary_expr(self)
        while(self.at(self).typeOf == TokenType.Dot or self.at(self).typeOf == TokenType.OpenBracket):
            operator = self.eat(self)
            prope = Expr
            comp = False
            if(operator.typeOf == TokenType.Dot):
                computed = False
                prope = self.parse_primary_expr(self)
                if(prope.kind != "Identifier"):
                    raise ValueError("Cannot use this operator withou RHS ident")
            else:
                computed = True
                prope = self.parse_expr(self)
                self.expect(self, TokenType.CloseBracket, "Expected closing bracket after computed value")
            objc = MemberExpr(kind="MemberExpr", obj=objc, prop=prope, computed=comp)   
             
        return objc  
        
        
    
    def parse_multiplicative_expr(self) -> Expr:
        leftt = self.parse_call_member_expr(self)
        while(self.at(self).value == "/" or self.at(self).value == "*" or self.at(self).value == "%"):
            #TODO change eat to expect
            operatorr = self.eat(self).value
            rightt = self.parse_call_member_expr(self)
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
        elif (tk == TokenType.Quotation):
            self.eat(self)
            val = ""
            if(self.at(self).typeOf != TokenType.Quotation and self.not_eof(self)):
                val = self.eat(self).value
                while(self.at(self).typeOf != TokenType.Quotation and self.not_eof(self)):
                    val += ' '
                    val += self.eat(self).value
            self.expect(self, TokenType.Quotation, "Close Quatation Error ")
            return StringLiteral(kind="StringLiteral", value=val)
        else:
            raise ValueError(f"unexpected token found during parsing {self.at(self)}")
            self.eat(self)
            
            


