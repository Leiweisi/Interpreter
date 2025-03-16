import re

class HHSInterpreter:
    def __init__(self):
        self.variables = {}
        self.functions = {}

    def evaluate_expression(self, expr):
        """ 簡單的表達式計算 """
        try:
            expr = expr.strip()
            for var in self.variables:
                expr = re.sub(r'\b' + re.escape(var) + r'\b', str(self.variables[var]), expr)

            return eval(expr, {}, {})
        except Exception as e:
            print(f"運算錯誤: {e}")
            return None

    def execute(self, code):
        """ 執行 HHS 程式碼 """
        lines = code.strip().split("\n")
        i = 0
        while i < len(lines):
            line = lines[i].strip()

            if not line:
                i += 1
                continue

            match = re.match(r'^([a-zA-Z_]\w*)(\+\+|--)$', line)
            if match:
                var_name = match.group(1)
                operator = match.group(2)
                if var_name in self.variables:
                    if operator == "++":
                        self.variables[var_name] += 1
                    elif operator == "--":
                        self.variables[var_name] -= 1
                else:
                    print(f"[錯誤] 變數 '{var_name}' 未宣告")
                i += 1
                continue


            
            # 變數
            match = re.match(r'^(let\s+)?([a-zA-Z_]\w*)\s*=\s*(.+)$', line)
            if match:
                var_name = match.group(2)
                value_expr = match.group(3).rstrip(";")
                value = self.evaluate_expression(value_expr)
                self.variables[var_name] = value
                i += 1
                continue

            # print
            match = re.match(r'^print\((.+)\)\s*$', line)
            if match:
                content = match.group(1).strip().strip('"')
                print(self.evaluate_expression(content) if content in self.variables else content)
                i += 1
                continue

            # if
            if line.startswith("if ") and line.endswith("{"):
                condition = line[3:-1].strip()
                if not self.evaluate_expression(condition):
                    i += 1
                    while i < len(lines) and "}" not in lines[i]:
                        i += 1
                i += 1
                continue

            # while
            if line.startswith("while ") and line.endswith("{"):
                condition = line[6:-1].strip()
                loop_start = i
                while self.evaluate_expression(condition):
                    i = loop_start + 1
                    while i < len(lines) and "}" not in lines[i]:
                        self.execute(lines[i])
                        i += 1
                    condition = line[6:-1].strip()
                i += 1
                continue

            # function
            if line.startswith("function "):
                func_name = line.split("(")[0][9:].strip()
                params = line.split("(")[1].split(")")[0].split(",")
                params = [p.strip() for p in params]
                self.functions[func_name] = (params, [])
                i += 1
                while i < len(lines) and "}" not in lines[i]:
                    self.functions[func_name][1].append(lines[i].strip())
                    i += 1
                i += 1
                continue

            # return
            if line.startswith("return "):
                return self.evaluate_expression(line[7:].rstrip(";"))

            i += 1


hhs_code = """
x = 10
print("Hello, World!")
if x > 5 {
    print("X is greater than 5")
}
while x > 0 {
    print(x)
    x = x - 1
}
while (x<10)  {
    print(x)
    x++
}
"""

interpreter = HHSInterpreter()
interpreter.execute(hhs_code)