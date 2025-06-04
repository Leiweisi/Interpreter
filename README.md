# 🐍 HHS 語言直譯器（HHS Interpreter）

HHS 是一個以 Python 開發的簡易直譯式程式語言，支援基礎數學運算、控制流程、函式、列表（list）、字串、錯誤檢查等功能。

---

## 📦 安裝方式

請依照你的使用情境，選擇以下其中一種安裝方式：

### ✅ 1. 一般本地安裝（從原始碼）

請打開終端機，**切換至專案根目錄**（即包含 `setup.py` 和 `pyproject.toml` 的資料夾，例如 `C:\hhs`），輸入：

```bash
pip install .
````

---

### 🔧 2. 開發模式安裝（推薦開發/測試用）

若你想在不重新安裝的情況下修改原始碼並立即測試，請使用：

```bash
pip install -e .
```

---

### 📦 3. 安裝已打包好的 `.whl` 或 `.tar.gz` 檔案

若你已使用 `python -m build` 打包成功，會在 `dist/` 目錄下出現：

```
dist/
├── hhs-0.1.0-py3-none-any.whl
└── hhs-0.1.0.tar.gz
```

你可以選擇其中一個安裝：

```bash
# 安裝 .whl 檔案
pip install dist/hhs-0.1.0-py3-none-any.whl

# 或安裝 .tar.gz 檔案
pip install dist/hhs-0.1.0.tar.gz
```

> ℹ️ `dist/` 是相對於目前終端機所在的路徑。

---

## 🚀 執行方式

安裝完成後，你可以在終端機使用 `hhs` 指令執行 `.hhs` 語言檔案，例如：

```bash
hhs examples/listTest.hhs
```

> ✅ 建議將 Python 加入 PATH，或在虛擬環境中執行。
> ✅ CLI 工具 `hhs` 會安裝到 Python 的 Scripts 目錄（例如：`~/.local/bin` 或 `C:\Users\使用者\AppData\Local\Programs\Python\Python311\Scripts`）。

---

## ✅ 語法支援功能

| 類型       | 說明                                       |   |    |
| -------- | ---------------------------------------- | - | -- |
| 變數與賦值    | `let x = 5;`，也可使用 `x = 5;`               |   |    |
| 數學運算     | `+ - * / %` 皆支援                          |   |    |
| 比較運算     | `== != < > <= >=`                        |   |    |
| 布林邏輯     | \`true false ! &&                       \`|   |  |
| 控制流程     | `if / else`、`while`                      |   |    |
| 區塊語句     | 使用 `{}` 包裹語句                             |   |    |
| 函式定義     | `function foo(a, b) { return a + b; }`   |   |    |
| 回傳值      | 使用 `return 表達式;`                         |   |    |
| 印出       | `print("字串", x, ...);` 支援多參數、混合類型輸出      |   |    |
| 列表（List） | `let l = [1, 2]; l[1] = 3; print(l[1]);` |   |    |
| 字串       | 支援單雙引號，例如 `"Hello"`、`'Hi'`               |   |    |
| 註解       | 使用 `#` 作為單行註解                            |   |    |
| 錯誤提示     | 未定義變數、索引錯誤會提示詳細錯誤訊息                      |   |    |

---

## 💡 範例程式

```hhs
# List 操作與邏輯判斷

let a = [1, 2, 3];
if (a[0] < 5) {
    print("第一個元素小於5：", a[0]);
}

function add(x, y) {
    return x + y;
}

let result = add(10, 20);
print("總和為", result);
```

---

## 📁 專案結構

```
C:\hhs
├─ hhs/               # 語言核心程式（ast, lexer, parser, interpreter）
├─ examples/          # 範例程式（.hhs）
├─ dist/              # 打包用（wheel/tar.gz）
├─ build/             # 安裝時產生的中繼檔案
├─ hhs_lang.egg-info/ # 套件資訊
├─ setup.py           # 套件安裝設定檔
├─ pyproject.toml     # PEP 517 建議格式（可選）
└─ README.md          # 使用說明文件
```

---

## 📌 注意事項

* ✅ 每行語句結尾需加 `;`
* ❌ 不支援 `f"..."` 字串插值語法，請使用 `print("字串", 變數)` 格式
* ⚠️ 當變數未定義或索引超出範圍時，會顯示清楚的錯誤訊息



