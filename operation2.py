class Interpreter:
    def evaluate(self, expr):
        if isinstance(expr, LogicalExpression):
            return self.evaluate_LogicalExpression(expr)
        elif isinstance(expr, UnaryExpression):
            return self.evaluate_UnaryExpression(expr)

    def evaluate_LogicalExpression(self, expr):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        if expr.operator == "and":
            return "TTT" if self.is_truthy(left) and self.is_truthy(right) else "FFF"
        elif expr.operator == "or":
            return "TTT" if self.is_truthy(left) or self.is_truthy(right) else "FFF"

    def evaluate_UnaryExpression(self, expr):
        right = self.evaluate(expr.right)
        if expr.operator == "not":
            return "TTT" if not self.is_truthy(right) else "FFF"

    def is_truthy(self, value):
        # 將 Python 的布林值轉換為 TTT/FFF
        if value == "true":
            return True
        elif value == "false":
            return False
        return bool(value)  # 其他值則按照常規布林值判斷


class LogicalExpression:
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

class UnaryExpression:
    def __init__(self, operator, right):
        self.operator = operator
        self.right = right


# 測試部分
interpreter = Interpreter()

# 示例： "true and false"
print(interpreter.evaluate(LogicalExpression("true", "and", "false")))  # Expected: FFF

# 示例： "true or false"
print(interpreter.evaluate(LogicalExpression("true", "or", "false")))  # Expected: TTT

# 示例： "not true"
print(interpreter.evaluate(UnaryExpression("not", "true")))            # Expected: FFF

# 示例： "not false"
print(interpreter.evaluate(UnaryExpression("not", "false")))           # Expected: TTT

# 示例： "1 and 0"
print(interpreter.evaluate(LogicalExpression("1", "and", "0")))        # Expected: FFF

# 示例： "0 or fallback"
print(interpreter.evaluate(LogicalExpression("0", "or", "fallback"))) # Expected: TTT
