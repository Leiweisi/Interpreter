# hhs/runtime_cli.py

import sys
from .runtime import run_hhs  

def main():
    if len(sys.argv) < 2:
        print("使用方法: hhs <檔案路徑>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    with open(file_path, 'r', encoding='utf-8') as f:
        code = f.read()
    
    run_hhs(code)
