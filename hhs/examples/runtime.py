from .lexer import lexer
from .parser import Parser
from .interpreter import Interpreter

def run_hhs(source_code):
    tokens = lexer(source_code)
    parser = Parser(tokens)
    ast = parser.parse()
    interpreter = Interpreter()
    interpreter.interpret(ast)