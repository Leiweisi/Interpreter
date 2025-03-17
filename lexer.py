import re

# Define token patterns
TOKEN_SPECIFICATION = [
    ('NUMBER', r'\d+(\.\d*)?'),     # Integer or decimal number
    ('STRING', r'"[^"]*"'),         # String in double quotes
    ('KEYWORD', r'\b(let|if|while|def|return|else)\b'), # Keywords
    ('IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_]*'), # Identifiers
    ('OPERATOR', r'[+\-*/=]'),      # Operators
    ('LOGICAL', r'&&|\|\|'),        # Logical operators
    ('COMPARISON', r'==|!=|<=|>=|<|>'), # Comparisons
    ('PUNCTUATION', r'[{}();]'),    # Braces, semicolons, etc.
    ('SKIP', r'[ \t]+'),            # Skip spaces/tabs
    ('NEWLINE', r'\n'),             # Newlines
]

# Compile regex patterns
TOKEN_REGEX = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in TOKEN_SPECIFICATION)

def lexer(code):
    tokens = []
    pos = 0  # 目前字元位置
    while pos < len(code):
        match = re.match(TOKEN_REGEX, code[pos:])
        if match:
            kind = match.lastgroup
            value = match.group()
            if kind != 'SKIP' and kind != 'NEWLINE':  # Ignore spaces and newlines
                tokens.append((kind, value))
            pos += len(value)  # 更新位置
        else:
            print(f"Lexer Error: Unrecognized token at position {pos}: {code[pos]}")
            pos += 1  # 跳過錯誤字元，避免死循環
    return tokens

# Test the lexer
source_code = '''
$%^ invalid_token
'''

print(lexer(source_code))
