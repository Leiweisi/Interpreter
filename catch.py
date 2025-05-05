# ==== AST 節點 ====
class ASTNode: pass

class Number(ASTNode):
    def __init__(self, value, line):
        self.value = value
        self.line = line

class VariableDeclaration(ASTNode):
    def __init__(self, name, value, line):
        self.name = name
        self.value = value
        self.line = line

class PrintStatement(ASTNode):
    def __init__(self, expr, line):
        self.expr = expr
        self.line = line

class BinaryExpression(ASTNode):
    def __init__(self, left, operator, right, line):
        self.left = left
        self.operator = operator
        self.right = right
        self.line = line

class String(ASTNode):
    def __init__(self, value, line):
        self.value = value
        self.line = line

class Variable(ASTNode):
    def __init__(self, name, line):
        self.name = name
        self.line = line

class TryCatchStatement(ASTNode):
    def __init__(self, try_body, catch_var, catch_body):
        self.try_body = try_body      # 語句列表
        self.catch_var = catch_var    # 字串
        self.catch_body = catch_body  # 語句列表

# ==== 錯誤類別 ====
class HHSError(Exception):
    def __init__(self, error_type, message, line=None):
        self.error_type = error_type
        self.message = message
        self.line = line
        super().__init__(f"{error_type} at line {line}: {message}" if line else f"{error_type}: {message}")

# ==== 變數作用域 ====
class Environment:
    def __init__(self, parent=None):
        self.values = {}
        self.parent = parent

    def define(self, name, value):
        self.values[name] = value

    def get(self, name, line=None):
        if name in self.values:
            return self.values[name]
        elif self.parent:
            return self.parent.get(name, line)
        else:
            raise HHSError("NameError", f"變數 '{name}' 未定義", line)

# ==== Interpreter ====
class Interpreter:
    def __init__(self):
        self.environment = Environment()

    def report_error(self, error):
        if error.line:
            print(f"【第{error.line}行】{error.error_type}：{error.message}")
        else:
            print(f"{error.error_type}：{error.message}")

    def execute(self, statements):
        try:
            for stmt in statements:
                self.execute_statement(stmt)
        except HHSError as err:
            self.report_error(err)

    def execute_statement(self, stmt):
        if isinstance(stmt, VariableDeclaration):
            value = self.evaluate(stmt.value)
            self.environment.define(stmt.name, value)
        elif isinstance(stmt, PrintStatement):
            value = self.evaluate(stmt.expr)
            print(value)
        elif isinstance(stmt, TryCatchStatement):
            self.evaluate_TryCatchStatement(stmt)
        else:
            raise HHSError("RuntimeError", "未知的語句型態", getattr(stmt, 'line', None))

    def evaluate(self, expr):
        if isinstance(expr, Number):
            return expr.value
        elif isinstance(expr, String):
            return expr.value
        elif isinstance(expr, Variable):
            return self.environment.get(expr.name, expr.line)
        elif isinstance(expr, BinaryExpression):
            left = self.evaluate(expr.left)
            right = self.evaluate(expr.right)
            op = expr.operator
            if op == '/':
                if not (isinstance(left, (int, float)) and isinstance(right, (int, float))):
                    raise HHSError("TypeError", "除法運算必須是數字型別", expr.line)
                if right == 0:
                    raise HHSError("RuntimeError", "Division by zero", expr.line)
                return left / right
            else:
                raise HHSError("RuntimeError", f"未知運算符 '{op}'", expr.line)
        else:
            raise HHSError("RuntimeError", "未知的運算式型態", getattr(expr, 'line', None))

    def evaluate_TryCatchStatement(self, node):
        try:
            for stmt in node.try_body:
                self.execute_statement(stmt)
        except HHSError as err:
            # catch 區塊建立新 scope，錯誤訊息變數存進去
            catch_env = Environment(parent=self.environment)
            catch_env.define(node.catch_var, err.message)
            # 執行 catch 區塊
            old_env = self.environment
            self.environment = catch_env
            try:
                for stmt in node.catch_body:
                    self.execute_statement(stmt)
            finally:
                self.environment = old_env

# ==== 測試案例 ====
# try {
#   let x = 1 / 0;
# } catch (e) {
#   print("Caught error: " + e);
# }

statements = [
    TryCatchStatement(
        try_body=[
            VariableDeclaration("x", BinaryExpression(Number(1, 2), "/", Number(0, 2), 2), 2)
        ],
        catch_var="e",
        catch_body=[
            PrintStatement(BinaryExpression(String("Caught error: ", 4), "+", Variable("e", 4), 4), 4)
        ]
    )
]

interpreter = Interpreter()
interpreter.execute(statements)
