class Interpreter:
    def evaluate(self, expr):
        if isinstance(expr, BinaryExpression):
            return self.evaluate_BinaryExpression(expr)
        elif isinstance(expr, LogicalExpression):
            return self.evaluate_LogicalExpression(expr)
        elif isinstance(expr, UnaryExpression):
            return self.evaluate_UnaryExpression(expr)
        # 其他情況處理...

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
        else:
            raise RuntimeError(f"Unknown operator: {expr.operator}")
print(3 == 3)   
print(3 != 4)    
print(5 > 2)
print(2 >= 2) 
print(7 < 1)   
print(9 <= 10)

