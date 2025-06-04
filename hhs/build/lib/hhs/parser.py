import re
from .ast import *
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def match(self, expected_type, expected_value=None):
        token = self.peek()
        if token and token[0] == expected_type and (expected_value is None or token[1] == expected_value):
            self.pos += 1
            return token
        return None

    def expect(self, expected_type, expected_value=None):
        token = self.match(expected_type, expected_value)
        if not token:
            expected = expected_value if expected_value else expected_type
            raise Exception(f'語法錯誤: 預期 {expected}')
        return token

    def parse(self):
        statements = []
        while self.pos < len(self.tokens):
            stmt = self.statement()
            statements.append(stmt)
        return statements

    def statement(self):
        token = self.peek()
        if token[0] == 'PUNCTUATION' and token[1] == '{':
            self.match('PUNCTUATION', '{')
            stmts = []
            while self.peek() and not (self.peek()[0] == 'PUNCTUATION' and self.peek()[1] == '}'):
                stmts.append(self.statement())
            self.expect('PUNCTUATION', '}')
            return Block(stmts)

        if token[0] == 'KEYWORD':
            if token[1] == 'let':
                self.match('KEYWORD', 'let')
                name = self.expect('IDENTIFIER')[1]
                self.expect('OPERATOR', '=')
                expr = self.expression()
                self.expect('PUNCTUATION', ';')
                return Assignment(name, expr)
            elif token[1] == 'print':
                self.match('KEYWORD', 'print')
                self.expect('PUNCTUATION', '(')
                exprs = []
                if self.peek() and not (self.peek()[0] == 'PUNCTUATION' and self.peek()[1] == ')'):
                    exprs.append(self.expression())
                    while self.peek() and self.peek()[0] == 'PUNCTUATION' and self.peek()[1] == ',':
                        self.match('PUNCTUATION', ',')
                        exprs.append(self.expression())
                self.expect('PUNCTUATION', ')')
                self.expect('PUNCTUATION', ';')
                return PrintStatement(exprs)
            

            elif token[1] == 'if':
                self.match('KEYWORD', 'if')
                self.expect('PUNCTUATION', '(')
                condition = self.expression()
                self.expect('PUNCTUATION', ')')
                then_branch = self.statement()
                else_branch = None
                if self.peek() and self.peek()[0] == 'KEYWORD' and self.peek()[1] == 'else':
                    self.match('KEYWORD', 'else')
                    else_branch = self.statement()
                return IfStatement(condition, then_branch, else_branch)
            elif token[1] == 'while':
                self.match('KEYWORD', 'while')
                self.expect('PUNCTUATION', '(')
                condition = self.expression()
                self.expect('PUNCTUATION', ')')
                body = self.statement()
                return WhileStatement(condition, body)
            elif token[1] == 'function':
                self.match('KEYWORD', 'function')
                name = self.expect('IDENTIFIER')[1]
                self.expect('PUNCTUATION', '(')
                params = []
                if self.peek() and self.peek()[0] == 'IDENTIFIER':
                    params.append(self.match('IDENTIFIER')[1])
                    while self.peek() and self.peek()[0] == 'PUNCTUATION' and self.peek()[1] == ',':
                        self.match('PUNCTUATION', ',')
                        params.append(self.expect('IDENTIFIER')[1])
                self.expect('PUNCTUATION', ')')
                body = self.statement()
                return FunctionDef(name, params, body)
            elif token[1] == 'return':
                self.match('KEYWORD', 'return')
                expr = self.expression()
                self.expect('PUNCTUATION', ';')
                return ReturnStatement(expr)

            else:
                raise Exception(f'未知的關鍵字: {token[1]}')

        if token[0] == 'IDENTIFIER':
            name = self.match('IDENTIFIER')[1]
    
            if self.peek() and self.peek()[0] == 'PUNCTUATION' and self.peek()[1] == '[':
                # list[index] = value;
                self.match('PUNCTUATION', '[')
                index = self.expression()
                self.expect('PUNCTUATION', ']')
                self.expect('OPERATOR', '=')
                value = self.expression()
                self.expect('PUNCTUATION', ';')
                return IndexAssignment(Variable(name), index, value)
    
            elif self.peek() and self.peek()[0] == 'PUNCTUATION' and self.peek()[1] == '(':
                # 函式呼叫語句
                self.match('PUNCTUATION', '(')
                args = []
                if self.peek() and not (self.peek()[0] == 'PUNCTUATION' and self.peek()[1] == ')'):
                    args.append(self.expression())
                    while self.peek() and self.peek()[0] == 'PUNCTUATION' and self.peek()[1] == ',':
                        self.match('PUNCTUATION', ',')
                        args.append(self.expression())
                self.expect('PUNCTUATION', ')')
                self.expect('PUNCTUATION', ';')
                return FunctionCall(name, args)
    
            else:
                # 普通變數賦值
                self.expect('OPERATOR', '=')
                expr = self.expression()
                self.expect('PUNCTUATION', ';')
                return Assignment(name, expr)

        try:
            expr = self.expression()
            self.expect('PUNCTUATION', ';')
            return ExpressionStatement(expr)
        except Exception:
            raise Exception(f'語法錯誤: 預期關鍵字，得到 {token}')
        

    def expression(self):
        return self.equality()
    
    def expression(self):
        return self.logic_or()

    def logic_or(self):
        node = self.logic_and()
        while self.peek() and self.peek()[0] == 'OPERATOR' and self.peek()[1] == '||':
            op = self.match('OPERATOR')[1]
            right = self.logic_and()
            node = BinaryOp(node, op, right)
        return node

    def logic_and(self):
        node = self.equality()
        while self.peek() and self.peek()[0] == 'OPERATOR' and self.peek()[1] == '&&':
            op = self.match('OPERATOR')[1]
            right = self.equality()
            node = BinaryOp(node, op, right)
        return node

    def equality(self):
        node = self.comparison()
        while True:
            token = self.peek()
            if token and token[0] == 'OPERATOR' and token[1] in ('==', '!='):
                op = self.match('OPERATOR')[1]
                right = self.comparison()
                node = BinaryOp(node, op, right)
            else:
                break
        return node

    def comparison(self):
        node = self.term()
        while True:
            token = self.peek()
            if token and token[0] == 'OPERATOR' and token[1] in ('<', '>', '<=', '>='):
                op = self.match('OPERATOR')[1]
                right = self.term()
                node = BinaryOp(node, op, right)
            else:
                break
        return node

    
    def term(self):
        node = self.factor()
        while True:
            token = self.peek()
            if token and token[0] == 'OPERATOR' and token[1] in ('+', '-'):
                op = self.match('OPERATOR')[1]
                right = self.factor()
                node = BinaryOp(node, op, right)
            else:
                break
        return node

    def factor(self):
        node = self.unary()
        while True:
            token = self.peek()
            if token and token[0] == 'OPERATOR' and token[1] in ('*', '/', '%'):
                op = self.match('OPERATOR')[1]
                right = self.unary()
                node = BinaryOp(node, op, right)
            else:
                break
        return node
    
    def unary(self):
        token = self.peek()
        if token and token[0] == 'OPERATOR' and token[1] in ('-', '!'):
            op = self.match('OPERATOR')[1]
            right = self.unary()
            return UnaryOp(op, right)
        else:
            return self.primary()

    def primary(self):
        token = self.peek()
        if token[0] == 'NUMBER':
            value = self.match('NUMBER')[1]
            return Number(value)
    
        elif token[0] == 'STRING':
            value = self.match('STRING')[1]
            return String(value[1:-1])  # 移除引號
    
        elif token[0] == 'IDENTIFIER':
            name = self.match('IDENTIFIER')[1]
            if self.peek() and self.peek()[0] == 'PUNCTUATION' and self.peek()[1] == '(':
                self.match('PUNCTUATION', '(')
                args = []
                if self.peek() and not (self.peek()[0] == 'PUNCTUATION' and self.peek()[1] == ')'):
                    args.append(self.expression())
                    while self.peek() and self.peek()[0] == 'PUNCTUATION' and self.peek()[1] == ',':
                        self.match('PUNCTUATION', ',')
                        args.append(self.expression())
                self.expect('PUNCTUATION', ')')
                return FunctionCall(name, args)
            if self.peek() and self.peek()[0] == 'PUNCTUATION' and self.peek()[1] == '[':
                self.match('PUNCTUATION', '[')
                index = self.expression()
                self.expect('PUNCTUATION', ']')
                return IndexAccess(Variable(name), index)
            else:
                return Variable(name)
    
        elif token[0] == 'PUNCTUATION' and token[1] == '(':
            self.match('PUNCTUATION', '(')
            expr = self.expression()
            self.expect('PUNCTUATION', ')')
            return expr
        elif token[0] == 'PUNCTUATION' and token[1] == '[':
            self.match('PUNCTUATION', '[')
            elements = []
            if self.peek() and not (self.peek()[0] == 'PUNCTUATION' and self.peek()[1] == ']'):
                elements.append(self.expression())
                while self.peek() and self.peek()[0] == 'PUNCTUATION' and self.peek()[1] == ',':
                    self.match('PUNCTUATION', ',')
                    elements.append(self.expression())
            self.expect('PUNCTUATION', ']')
            return ListLiteral(elements)

        elif token[0] == 'KEYWORD' and token[1] in ('true', 'false'):
            value = self.match('KEYWORD')[1]
            return Boolean(value == 'true')

        else:
            raise Exception(f'語法錯誤: 無效的主表達式 {token}')