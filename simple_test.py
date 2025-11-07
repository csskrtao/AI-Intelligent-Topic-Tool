import sys
sys.stdout.reconfigure(encoding='utf-8')

print("测试开始")

from src.utils import parse_deepseek_ocr_response

test_content = """<|ref|>text<|/ref|><|det|>[[36, 25, 912, 185]]<|/det|>       
42.(10分)现有题目内容"""

print("解析中...")
blocks = parse_deepseek_ocr_response(test_content)
print(f"解析出 {len(blocks)} 个文本块")

for i, block in enumerate(blocks):
    print(f"块 {i+1}: {block}")

