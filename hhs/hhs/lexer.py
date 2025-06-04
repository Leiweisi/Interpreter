import re

# Token 類型
TOKEN_TYPES = [
    ('COMMENT',     r'#.*'),
    ('STRING',      r'(\".*?\"|\'.*?\')'),  # 支援單/雙引號字串
    ('NUMBER',      r'\d+(\.\d+)?'),
    ('IDENTIFIER',  r'[A-Za-z_]\w*'),
    ('OPERATOR',    r'==|!=|<=|>=|\|\||&&|[+\-*/%<>=!]'),
    ('PUNCTUATION', r'[()\[\]{},;]'),
    ('WHITESPACE',  r'\s+'),
]

# 關鍵字
KEYWORDS = {'let', 'print', 'if', 'else', 'while', 'function', 'return','true','false'}

# 詞法分析器
def lexer(code):
    tokens = []
    pos = 0
    while pos < len(code):
        current = code[pos]

        if current in ' \t\n\r':
            pos += 1
            continue

        match = None
        for token_type, pattern in TOKEN_TYPES:
            regex = re.compile(pattern)
            match = regex.match(code, pos)
            if match:
                text = match.group(0)
                if token_type in ('WHITESPACE', 'COMMENT'):
                    pass  
                elif token_type == 'IDENTIFIER' and text.lower() in KEYWORDS:
                    tokens.append(('KEYWORD', text.lower()))
                else:
                    tokens.append((token_type, text))
                pos = match.end()
                break

        if not match:
            raise Exception(f'無法解析的字元: {code[pos]}')
    return tokens
