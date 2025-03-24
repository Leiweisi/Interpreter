# ---------------------------
# AST 節點類別定義（擴充版）
# ---------------------------
class ASTNode:
    pass

class Number(ASTNode):
    def __init__(self, value):
        self.value = value

class String(ASTNode):
    def __init__(self, value):
        self.value = value

class Variable(ASTNode):
    def __init__(self, name):
        self.name = name

class BinaryExpression(ASTNode):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator  # 以字串表示，例如 "+", "*", ">" 等
        self.right = right

class VarDeclaration(ASTNode):
    def __init__(self, name, value):
        self.name = name
        self.value = value

class IfStatement(ASTNode):
    def __init__(self, condition, then_branch, else_branch=None):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

class WhileStatement(ASTNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class FunctionCall(ASTNode):
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments

class Block(ASTNode):
    def __init__(self, statements):
        self.statements = statements

# ---------------------------
# Parser 類別定義（修改後，新增 block() 方法）
# ---------------------------
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def match(self, *token_types):
        if self.peek() and self.peek()[0] in token_types:
            return self.advance()
        return None

    def peek(self):
        return self.tokens[self.current] if self.current < len(self.tokens) else None

    def advance(self):
        self.current += 1
        return self.tokens[self.current - 1]

    def consume(self, token_type, error_message):
        if self.peek() and self.peek()[0] == token_type:
            return self.advance()
        raise Exception(error_message)

    # 新增 block() 方法來解析區塊：以 "{" 開始，以 "}" 結束
    def block(self):
        self.consume("LEFT_BRACE", "期望 '{' 開始區塊")
        statements = []
        while self.peek() and self.peek()[0] != "RIGHT_BRACE":
            statements.append(self.statement())
        self.consume("RIGHT_BRACE", "期望 '}' 結束區塊")
        return Block(statements)

    # 修改 statement()，若遇到區塊開頭則呼叫 block() 解析
    def statement(self):
        token = self.peek()
        if token:
            if token[0] == "LEFT_BRACE":
                return self.block()
            if token[0] == "KEYWORD":
                if token[1] == "if":
                    return self.if_statement()
                elif token[1] == "while":
                    return self.while_statement()
                elif token[1] == "let":
                    self.advance()  # 消費 "let"
                    return self.var_declaration(with_keyword=True)
            if token[0] == "IDENTIFIER":
                # 檢查識別字後是否跟 "=" (變數宣告，省略 let)
                if self.current + 1 < len(self.tokens) and \
                   self.tokens[self.current + 1][0] == "OPERATOR" and self.tokens[self.current + 1][1] == "=":
                    return self.var_declaration(with_keyword=False)
        return self.expression_statement()

    def var_declaration(self, with_keyword):
        if with_keyword:
            identifier = self.consume("IDENTIFIER", "期望變數名稱")
        else:
            identifier = self.advance()
        self.consume("OPERATOR", "期望 '=' 於變數宣告中")
        expression = self.expression()
        self.match("PUNCTUATION")  # 分號可有可無
        return VarDeclaration(identifier[1], expression)

    def expression_statement(self):
        expr = self.expression()
        self.match("PUNCTUATION")
        return expr

    def expression(self):
        return self.equality()

    def equality(self):
        node = self.comparison()
        while self.peek() and self.peek()[0] in ("EQUAL", "NOT_EQUAL"):
            operator = self.advance()[1]
            right = self.comparison()
            node = BinaryExpression(node, operator, right)
        return node

    def comparison(self):
        node = self.term()
        while self.peek() and self.peek()[0] in ("GREATER", "LESS", "GREATER_EQUAL", "LESS_EQUAL"):
            operator = self.advance()[1]
            right = self.term()
            node = BinaryExpression(node, operator, right)
        return node

    def term(self):
        node = self.factor()
        while self.peek() and self.peek()[0] in ("PLUS", "MINUS"):
            operator = self.advance()[1]
            right = self.factor()
            node = BinaryExpression(node, operator, right)
        return node

    def factor(self):
        node = self.unary()
        while self.peek() and self.peek()[0] in ("MULTIPLY", "DIVIDE"):
            operator = self.advance()[1]
            right = self.unary()
            node = BinaryExpression(node, operator, right)
        return node

    def unary(self):
        if self.peek() and self.peek()[0] in ("NOT", "MINUS"):
            operator = self.advance()[1]
            operand = self.unary()
            return BinaryExpression(None, operator, operand)
        return self.primary()

    def primary(self):
        token = self.peek()
        if token is None:
            raise Exception("意外結尾：缺少表達式")
        if token[0] == "NUMBER":
            self.advance()
            return Number(token[1])
        if token[0] == "STRING":
            self.advance()
            return String(token[1])
        if token[0] == "IDENTIFIER":
            self.advance()
            node = Variable(token[1])
            if self.peek() and self.peek()[0] == "LEFT_PAREN":
                node = self.function_call(node)
            return node
        if token[0] == "LEFT_PAREN":
            self.advance()
            expr = self.expression()
            self.consume("RIGHT_PAREN", "期望 ')' 結束表達式")
            return expr
        raise Exception(f"無法識別的 token: {token}")

    def function_call(self, callee):
        self.consume("LEFT_PAREN", "期望 '(' 開始函數參數列表")
        arguments = []
        if self.peek() and self.peek()[0] != "RIGHT_PAREN":
            arguments.append(self.expression())
            while self.peek() and self.peek()[0] == "COMMA":
                self.advance()  # 消費逗號
                arguments.append(self.expression())
        self.consume("RIGHT_PAREN", "期望 ')' 結束函數參數列表")
        return FunctionCall(callee, arguments)

    def if_statement(self):
        self.advance()  # 消費 "if"
        self.consume("LEFT_PAREN", "期望 '(' 開始 if 條件")
        condition = self.expression()
        self.consume("RIGHT_PAREN", "期望 ')' 結束 if 條件")
        then_branch = self.statement()
        else_branch = None
        if self.peek() and self.peek()[0] == "KEYWORD" and self.peek()[1] == "else":
            self.advance()  # 消費 "else"
            else_branch = self.statement()
        return IfStatement(condition, then_branch, else_branch)

    def while_statement(self):
        self.advance()  # 消費 "while"
        self.consume("LEFT_PAREN", "期望 '(' 開始 while 條件")
        condition = self.expression()
        self.consume("RIGHT_PAREN", "期望 ')' 結束 while 條件")
        body = self.statement()
        return WhileStatement(condition, body)

    def parse(self):
        statements = []
        while self.current < len(self.tokens):
            statements.append(self.statement())
        return statements

# ---------------------------
# 測試案例
# ---------------------------

# Test 1: Simple Expression  (解析 5 + 3 * 2;)
tokens_test1 = [
    ("NUMBER", "5"),
    ("PLUS", "+"),
    ("NUMBER", "3"),
    ("MULTIPLY", "*"),
    ("NUMBER", "2"),
    ("PUNCTUATION", ";")
]

# Test 2: If Statement
# 解析 if (x > 5) { print("X is large"); }
tokens_test2 = [
    ("KEYWORD", "if"),
    ("LEFT_PAREN", "("),
    ("IDENTIFIER", "x"),
    ("GREATER", ">"),
    ("NUMBER", "5"),
    ("RIGHT_PAREN", ")"),
    ("LEFT_BRACE", "{"),           # 使用 { 表示區塊開始
    ("IDENTIFIER", "print"),
    ("LEFT_PAREN", "("),
    ("STRING", "X is large"),
    ("RIGHT_PAREN", ")"),
    ("RIGHT_BRACE", "}")           # 使用 } 表示區塊結束
]

# Test 3: Variable Declaration  (解析 let x = 42;)
tokens_test3 = [
    ("KEYWORD", "let"),
    ("IDENTIFIER", "x"),
    ("OPERATOR", "="),
    ("NUMBER", "42"),
    ("PUNCTUATION", ";")
]

# ---------------------------
# 印出 AST 結構的輔助函式
# ---------------------------
def print_ast(node, indent=0):
    prefix = " " * indent
    if isinstance(node, VarDeclaration):
        print(f"{prefix}VarDeclaration(identifier={node.name})")
        print(f"{prefix} Expression:")
        print_ast(node.value, indent + 4)
    elif isinstance(node, IfStatement):
        print(f"{prefix}IfStatement")
        print(f"{prefix} Condition:")
        print_ast(node.condition, indent + 4)
        print(f"{prefix} Then:")
        print_ast(node.then_branch, indent + 4)
        if node.else_branch:
            print(f"{prefix} Else:")
            print_ast(node.else_branch, indent + 4)
    elif isinstance(node, WhileStatement):
        print(f"{prefix}WhileStatement")
        print(f"{prefix} Condition:")
        print_ast(node.condition, indent + 4)
        print(f"{prefix} Body:")
        print_ast(node.body, indent + 4)
    elif isinstance(node, FunctionCall):
        print(f"{prefix}FunctionCall(callee={node.name.name if isinstance(node.name, Variable) else node.name})")
        print(f"{prefix} Arguments:")
        for arg in node.arguments:
            print_ast(arg, indent + 4)
    elif isinstance(node, BinaryExpression):
        print(f"{prefix}BinaryExpression(operator={node.operator})")
        print(f"{prefix} Left:")
        print_ast(node.left, indent + 4)
        print(f"{prefix} Right:")
        print_ast(node.right, indent + 4)
    elif isinstance(node, Block):
        print(f"{prefix}Block:")
        for stmt in node.statements:
            print_ast(stmt, indent + 4)
    elif isinstance(node, Variable):
        print(f"{prefix}Variable(name={node.name})")
    elif isinstance(node, Number):
        print(f"{prefix}Number(value={node.value})")
    elif isinstance(node, String):
        print(f"{prefix}String(value={node.value})")
    else:
        print(f"{prefix}{node}")

# ---------------------------
# 測試執行函式
# ---------------------------
def test_parser(tokens, test_name):
    print(f"=== {test_name} ===")
    parser = Parser(tokens)
    try:
        ast_nodes = parser.parse()
        for stmt in ast_nodes:
            print_ast(stmt)
    except Exception as e:
        print("解析錯誤：", e)
    print("\n")

# 執行三個測試案例
test_parser(tokens_test1, "Test 1: Simple Expression")
test_parser(tokens_test2, "Test 2: If Statement")
test_parser(tokens_test3, "Test 3: Variable Declaration")
