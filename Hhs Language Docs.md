# 📘 HHS 語言專案文件

---

## 一、語言文法（BNF）

```bnf
<program>       ::= <statement>*
<statement>     ::= <assignment> | <print> | <if> | <while> | <function_def> | <return> | <expression_stmt> | <block> | <index_assignment>
<block>         ::= "{" <statement>* "}"
<assignment>    ::= ["let"] <identifier> "=" <expression> ";"
<print>         ::= "print" "(" <expression_list> ")" ";"
<if>            ::= "if" "(" <expression> ")" <statement> ["else" <statement>]
<while>         ::= "while" "(" <expression> ")" <statement>
<function_def>  ::= "function" <identifier> "(" [<identifier_list>] ")" <block>
<return>        ::= "return" <expression> ";"
<expression_stmt>::= <expression> ";"
<expression_list>::= <expression> ["," <expression>]*
<identifier_list>::= <identifier> ["," <identifier>]*
<expression>    ::= <logical_or>
<logical_or>    ::= <logical_and> {"||" <logical_and>}
<logical_and>   ::= <equality> {"&&" <equality>}
<equality>      ::= <relational> (("==" | "!=" ) <relational>)*
<relational>    ::= <term> (("<" | ">" | "<=" | ">=") <term>)*
<term>          ::= <factor> (("+" | "-") <factor>)*
<factor>        ::= <unary> (("*" | "/" | "%") <unary>)*
<unary>         ::= ["-" | "!"] <primary>
<primary>       ::= <number> | <string> | <boolean> | <identifier> | <list_literal> | <function_call> | <index_access> | "(" <expression> ")"
<function_call> ::= <identifier> "(" [<expression_list>] ")"
<list_literal>  ::= "[" [<expression_list>] "]"
<index_access>  ::= <identifier> "[" <expression> "]"
<index_assignment> ::= <identifier> "[" <expression> "]" "=" <expression> ";"

<number>        ::= 數字（整數或浮點數）
<string>        ::= 雙引號或單引號包住的字串
<boolean>       ::= "true" | "false"
<identifier>    ::= 變數或函式名稱（字母開頭，允許數字與底線）
```

---

## 二、直譯器設計文檔

### 1. 模組結構

* `lexer.py`：負責將原始碼轉換為 Token 序列（支援註解、數字、字串、運算子等）
* `parser.py`：將 Token 序列解析成 AST 結構（支援 if、while、function 等語法）
* `ast.py`：定義 AST 各種節點類型（如 `BinaryOp`, `FunctionDef`, `ListLiteral`）
* `interpreter.py`：執行 AST，實現語義動作與執行環境（作用域、函式呼叫、錯誤處理）
* `runtime.py` / `runtime_cli.py`：提供執行入口與 CLI 命令 `hhs` 支援

### 2. 語法解析器設計（Parser）

* 遞迴下降方式設計
* 每種語法（statement, expression, primary 等）皆對應一個 parser 函式
* 使用 `peek` 與 `match` 檢查當前 Token，控制語法流程
* 支援運算子優先順序與括號巢狀結構

### 3. 執行引擎設計（Interpreter）

* 以 `self.env` 字典作為執行環境儲存變數
* 支援區塊作用域（函式呼叫時複製作用域）
* `evaluate()` 評估表達式，`execute()` 執行語句
* 支援錯誤提示（未定義變數、索引超出、參數不符）

---

## 三、HHS 程式語言使用手冊

### 1. 關鍵字

* `let`, `if`, `else`, `while`, `function`, `return`, `print`, `true`, `false`

### 2. 資料型別

* 數字（整數與浮點數）
* 字串：`"Hello"` 或 `'Hi'`
* 布林：`true` / `false`
* 列表（List）：`[1, 2, 3]`

### 3. 運算子

| 類型 | 運算子                              |   |    |
| -- | -------------------------------- | - | -- |
| 算術 | `+`, `-`, `*`, `/`, `%`          |   |    |
| 比較 | `==`, `!=`, `<`, `>`, `<=`, `>=` |   |    |
| 邏輯 | `!`, `&&`, \`                    |   | \` |
| 其他 | `[]`（索引）                         |   |    |

### 4. 控制結構

```hhs
let x = 10;
if (x > 5) {
    print("大於5");
} else {
    print("小於等於5");
}

while (x > 0) {
    print(x);
    x = x - 1;
}
```

### 5. 函式與回傳

```hhs
function square(n) {
    return n * n;
}
print(square(4));  # 印出 16
```

### 6. 錯誤處理（內建）

* 未定義變數：`Exception: 未定義的變數 x`
* 索引錯誤：`Exception: 索引超出範圍: l[5]`
* 函式參數不符：`Exception: 函式參數數量不符`

---

## 四、測試用例（Test Cases）

```hhs
# ✅ 測試 1：變數與數學運算
let x = 5;
let y = 3;
print(x + y);  # 預期輸出：8

# ✅ 測試 2：邏輯判斷與布林
if (x > y) {
    print("x 比 y 大");
} else {
    print("x 比 y 小或相等");
}

# ✅ 測試 3：函式與回傳
function mul(a, b) {
    return a * b;
}
print(mul(3, 4));  # 預期輸出：12

# ✅ 測試 4：列表操作與索引
let l = [10, 20, 30];
print(l[1]);       # 預期輸出：20
l[1] = 99;
print(l[1]);       # 預期輸出：99

# ✅ 測試 5：錯誤測試
print(z);          # 預期錯誤：未定義變數
print(l[10]);      # 預期錯誤：索引超出範圍
```

---

> 如需完整測試程式，請參見 `examples/` 資料夾。
