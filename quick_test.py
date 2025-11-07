#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, '.')

from src.utils import parse_deepseek_ocr_response

test = """<|ref|>text<|/ref|><|det|>[[36, 25, 912, 185]]<|/det|>       
42.(10分)现有题目"""

result = parse_deepseek_ocr_response(test)
print(f"Blocks: {len(result)}")
for b in result:
    print(f"Box: {b['box']}, Text: {b['text']}")

