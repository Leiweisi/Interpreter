# ------------ AST 節點定義 ------------
class ASTNode: pass

class Number(ASTNode):
    def __init__(self, value): self.value = value
    def __repr__(self): return f"Number({self.value})"

class String(ASTNode):
    def __init__(self, value): self.value = value
    def __repr__(self): return f"String('{self.value}')"

class Variable(ASTNode):
    def __init__(self, name): self.name = name
    def __repr__(self): return f"Variable('{self.name}')"

class BinaryExpression(ASTNode):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right
    def __repr__(self): 
        return f"Binary({self.left} {self.operator} {self.right})"

class VariableDeclaration(ASTNode):
    def __init__(self, name, value):
        self.name = name
        self.value = value
    def __repr__(self): return f"Let({self.name} = {self.value})"

class Assignment(ASTNode):
    def __init__(self, name, value):
        self.name = name
        self.value = value
    def __repr__(self): return f"Assign({self.name} = {self.value})"

class IfStatement(ASTNode):
    def __init__(self, condition, then_branch, else_branch=None):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch
    def __repr__(self): 
        return f"If({self.condition}) {{ {self.then_branch} }} else {{ {self.else_branch} }}"

class WhileLoop(ASTNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body
    def __repr__(self): return f"While({self.condition}) {{ {self.body} }}"

class Block(ASTNode):
    def __init__(self, statements):
        self.statements = statements
    def __repr__(self): 
        return "Block[" + "; ".join(map(str, self.statements)) + "]"

class PrintStatement(ASTNode):
    def __init__(self, expression):
        self.expression = expression
    def __repr__(self): return f"Print({self.expression})"

class FunctionCall(ASTNode):
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments
    def __repr__(self): 
        args = ", ".join(map(str, self.arguments))
        return f"{self.name}({args})"

# ------------ Interpreter 解釋器 ------------
class Interpreter:
    def __init__(self):
        self.environment = {}
        self.functions = {
            "print": lambda x: print(x)
        }

    def evaluate(self, node):
        if isinstance(node, Number):
            return node.value
        elif isinstance(node, String):
            return node.value
        elif isinstance(node, Variable):
            value = self.environment.get(node.name)
            if value is None:
                raise NameError(f"變數未定義: {node.name}")
            return value
        elif isinstance(node, BinaryExpression):
            left = self.evaluate(node.left)
            right = self.evaluate(node.right)
            if node.operator == "+": return left + right
            elif node.operator == "-": return left - right
            elif node.operator == "*": return left * right
            elif node.operator == "/": 
                if right == 0:
                    raise ZeroDivisionError("除數不能為零")
                return left / right
            elif node.operator == ">": return left > right
            elif node.operator == "<": return left < right
            elif node.operator == "==": return left == right
            else:
                raise ValueError(f"不支援的運算符: {node.operator}")
        elif isinstance(node, VariableDeclaration):
            self.environment[node.name] = self.evaluate(node.value)
        elif isinstance(node, Assignment):
            if node.name not in self.environment:
                raise NameError(f"變數未定義: {node.name}")
            self.environment[node.name] = self.evaluate(node.value)
        elif isinstance(node, IfStatement):
            if self.evaluate(node.condition):
                return self.evaluate(node.then_branch)
            elif node.else_branch:
                return self.evaluate(node.else_branch)
        elif isinstance(node, WhileLoop):
            while self.evaluate(node.condition):
                self.evaluate(node.body)
        elif isinstance(node, Block):
            for stmt in node.statements:
                self.evaluate(stmt)
        elif isinstance(node, PrintStatement):
            value = self.evaluate(node.expression)
            print(value)
        elif isinstance(node, FunctionCall):
            func = self.functions.get(node.name)
            if func is None:
                raise NameError(f"函數未定義: {node.name}")
            args = [self.evaluate(arg) for arg in node.arguments]
            return func(*args)
        else:
            raise TypeError(f"未知節點類型: {type(node)}")

    def interpret(self, ast):
        for node in ast:
            try:
                result = self.evaluate(node)
                if result is not None and not isinstance(node, (PrintStatement, FunctionCall)):
                    print(f"Result: {result}")
            except Exception as e:
                print(f"執行錯誤: {e}")
                break

# ------------ 測試案例 ------------
if __name__ == "__main__":
    # 測試案例 1: 基本算術
    print("\n=== Test 1: Basic Arithmetic ===")
    test1 = BinaryExpression(Number(5), "+", Number(3))
    interpreter = Interpreter()
    interpreter.interpret([test1])  # 預期輸出: 8

    # 測試案例 2: 變數宣告與賦值
    print("\n=== Test 2: Variable Declaration & Assignment ===")
    test2 = [
        VariableDeclaration("x", Number(10)),
        Assignment("x", BinaryExpression(Number(10), "+", Number(5)))
    ]
    interpreter = Interpreter()
    interpreter.interpret(test2)
    print(f"x = {interpreter.environment.get('x')}")  # 預期輸出: x = 15

    # 測試案例 3: If 語句
    print("\n=== Test 3: If Statement ===")
    test3 = IfStatement(
        BinaryExpression(Number(5), ">", Number(3)),
        PrintStatement(String("Condition met"))
    )
    interpreter = Interpreter()
    interpreter.interpret([test3])  # 預期輸出: Condition met

    # 測試案例 4: While 循環
    print("\n=== Test 4: While Loop ===")
    test4 = [
        VariableDeclaration("x", Number(3)),
        WhileLoop(
            BinaryExpression(Variable("x"), ">", Number(0)),
            Block([
                PrintStatement(Variable("x")),
                Assignment("x", BinaryExpression(Variable("x"), "-", Number(1)))
            ])
        )
    ]
    interpreter = Interpreter()
    interpreter.interpret(test4)  # 預期輸出: 3 2 1 (每行一個數字)