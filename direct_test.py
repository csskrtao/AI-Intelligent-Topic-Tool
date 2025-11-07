# -*- coding: utf-8 -*-
import re
import json
import sys

# Reload the module to get latest changes
sys.path.insert(0, '.')
import importlib
if 'src.utils' in sys.modules:
    importlib.reload(sys.modules['src.utils'])

from src.utils import parse_deepseek_ocr_response

test_content = """<|ref|>text<|/ref|><|det|>[[36, 25, 912, 185]]<|/det|>       
42.(10分)现有题目
<|ref|>text<|/ref|><|det|>[[67, 194, 914, 345]]<|/det|>      
（1）设计一个算法"""

print("Testing parse_deepseek_ocr_response...")
print("=" * 60)

blocks = parse_deepseek_ocr_response(test_content)

print(f"Parsed {len(blocks)} blocks")
print()

for i, block in enumerate(blocks, 1):
    print(f"Block {i}:")
    print(f"  Box: {block['box']}")
    print(f"  Text: {block['text'][:50]}...")
    print()

if len(blocks) > 0:
    print("SUCCESS!")
else:
    print("FAILED - no blocks parsed")

