import re

class ASTNode:
    pass

class Number(ASTNode):
    def __init__(self, value):
        self.value = float(value)

class Variable(ASTNode):
    def __init__(self, name):
        self.name = name

class BinaryOp(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class Assignment(ASTNode):
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr

class PrintStatement(ASTNode):
    def __init__(self, expressions):
        self.expressions = expressions

class ReturnStatement(ASTNode):
    def __init__(self, expr):
        self.expr = expr

class IfStatement(ASTNode):
    def __init__(self, condition, then_branch, else_branch=None):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

class WhileStatement(ASTNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class Block(ASTNode):
    def __init__(self, statements):
        self.statements = statements

class FunctionDef(ASTNode):
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

class FunctionCall(ASTNode):
    def __init__(self, name, args):
        self.name = name
        self.args = args

class Boolean(ASTNode):
    def __init__(self, value):
        self.value = value  # True or False

class UnaryOp(ASTNode):
    def __init__(self, op, expr):
        self.op = op
        self.expr = expr

class ExpressionStatement:
    def __init__(self, expression):
        self.expression = expression

class String(ASTNode):
    def __init__(self, value):
        self.value = value

class ListLiteral(ASTNode):
    def __init__(self, elements):
        self.elements = elements

class IndexAccess(ASTNode):
    def __init__(self, collection, index):
        self.collection = collection
        self.index = index

class IndexAssignment(ASTNode):
    def __init__(self, collection, index, value):
        self.collection = collection
        self.index = index
        self.value = value

      