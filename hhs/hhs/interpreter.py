import re
from .ast import *
class Interpreter:
    def __init__(self):
        self.env = {}
        self.functions = {}
        self.returning = False
        self.return_value = None

    def interpret(self, statements):
        for stmt in statements:
            self.execute(stmt)

    def execute(self, node):
        if isinstance(node, Assignment):
            value = self.evaluate(node.expr)
            self.env[node.name] = value
        elif isinstance(node, PrintStatement):
            values = [self.evaluate(expr) for expr in node.expressions]
            print(*values)  
        elif isinstance(node, IfStatement):
            condition_value = self.evaluate(node.condition)
            if condition_value:
                self.execute(node.then_branch)
            elif node.else_branch:
                self.execute(node.else_branch)
        elif isinstance(node, WhileStatement):
            while self.evaluate(node.condition):
                self.execute(node.body)
        elif isinstance(node, Block):
            for stmt in node.statements:
                self.execute(stmt)
                if self.returning:
                    break
        elif isinstance(node, FunctionDef):
            self.functions[node.name] = node
        elif isinstance(node, FunctionCall):
            self.evaluate(node)  # 呼叫函式但不使用回傳值
        elif isinstance(node, ReturnStatement):
            self.return_value = self.evaluate(node.expr)
            self.returning = True
        elif isinstance(node, IndexAssignment):
            collection = self.evaluate(node.collection)
            index = int(self.evaluate(node.index))
            value = self.evaluate(node.value)
            if not isinstance(collection, list):
                raise TypeError(f"[錯誤] 只能對列表使用索引賦值")
            if index < 0 or index >= len(collection):
                raise IndexError(f"[錯誤] 賦值索引超出範圍：index={index}, 長度={len(collection)}")
            collection[index] = value
        else:
            raise Exception(f'無法執行的語句: {node}')

    def evaluate(self, node):
        if isinstance(node, Number):
            return node.value
        elif isinstance(node, Variable):
            if node.name in self.env:
                return self.env[node.name]
            else:
                raise NameError(f"[錯誤] 嘗試存取未定義的變數：'{node.name}'")
        elif isinstance(node, BinaryOp):
            left = self.evaluate(node.left)
            right = self.evaluate(node.right)
            if node.op == '+':
                return left + right
            elif node.op == '-':
                return left - right
            elif node.op == '*':
                return left * right
            elif node.op == '/':
                return left / right
            elif node.op == '%':
                return left % right
            elif node.op == '==':
                return left == right
            elif node.op == '!=':
                return left != right
            elif node.op == '<':
                return left < right
            elif node.op == '>':
                return left > right
            elif node.op == '<=':
                return left <= right
            elif node.op == '>=':
                return left >= right
            elif node.op == '&&':
                return bool(left) and bool(right)
            elif node.op == '||':
                return bool(left) or bool(right)
            else:
                raise Exception(f'未知的運算子: {node.op}')
            
        elif isinstance(node, FunctionCall):
            func = self.functions.get(node.name)
            if not func:
                raise Exception(f'未定義的函式: {node.name}')
            if len(func.params) != len(node.args):
                raise Exception(f'函式參數數量不符: {node.name}')
            local_env = self.env.copy()
            for param, arg in zip(func.params, node.args):
                local_env[param] = self.evaluate(arg)
            saved_env = self.env
            self.env = local_env
            self.returning = False
            self.return_value = None
            self.execute(func.body)
            result = self.return_value
            self.returning = False
            self.return_value = None
            self.env = saved_env
            return result
        elif isinstance(node, Boolean):
            return node.value

        elif isinstance(node, UnaryOp):
            operand = self.evaluate(node.expr)
            if node.op == '!':
                return not bool(operand)
            elif node.op == '-':
                return -operand
            else:
                raise Exception(f'未知的單元運算子: {node.op}')
        elif isinstance(node, String):
            return node.value
        elif isinstance(node, ListLiteral):
            return [self.evaluate(e) for e in node.elements]
        elif isinstance(node, IndexAccess):
            collection = self.evaluate(node.collection)
            index = int(self.evaluate(node.index))
            if not isinstance(collection, list):
                raise TypeError(f"[錯誤] 嘗試索引非列表物件：{collection}")
            if index < 0 or index >= len(collection):
                raise IndexError(f"[錯誤] 索引超出範圍：index={index}, 長度={len(collection)}")
            return collection[index]
        else:
            raise Exception(f'無法評估的節點: {node}')