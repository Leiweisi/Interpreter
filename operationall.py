class Interpreter:
    def evaluate(self, expr):
        if isinstance(expr, str) or isinstance(expr, (int, float)):
            return expr

        if isinstance(expr, LogicalExpression):
            return self.evaluate_LogicalExpression(expr)
        elif isinstance(expr, UnaryExpression):
            return self.evaluate_UnaryExpression(expr)
        elif isinstance(expr, BinaryExpression):
            return self.evaluate_BinaryExpression(expr)

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

    def evaluate_BinaryExpression(self, expr):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        if expr.operator == "==":
            return "TTT" if left == right else "FFF"
        elif expr.operator == "!=":
            return "TTT" if left != right else "FFF"
        elif expr.operator == "<":
            return "TTT" if left < right else "FFF"
        elif expr.operator == "<=":
            return "TTT" if left <= right else "FFF"
        elif expr.operator == ">":
            return "TTT" if left > right else "FFF"
        elif expr.operator == ">=":
            return "TTT" if left >= right else "FFF"

    def is_truthy(self, value):
        if isinstance(value, str):
            value = value.lower()
        if value == "true":
            return True
        elif value == "false":
            return False
        return bool(value)


class LogicalExpression:
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right


class UnaryExpression:
    def __init__(self, operator, right):
        self.operator = operator
        self.right = right


class BinaryExpression:
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right


def main():
    interpreter = Interpreter()

    x = 5
    y = 10

    expr1 = LogicalExpression(
        BinaryExpression(x, "<", y),
        "and",
        BinaryExpression(x, "!=", 0)
    )
    result1 = interpreter.evaluate(expr1)
    if result1 == "TTT":
        print("x is less and nonzero")

    expr2 = LogicalExpression(
        BinaryExpression(x, "==", 5),
        "or",
        BinaryExpression(y, "==", 5)
    )
    result2 = interpreter.evaluate(expr2)
    if result2 == "TTT":
        print("One of them is five")


if __name__ == "__main__":
    main()