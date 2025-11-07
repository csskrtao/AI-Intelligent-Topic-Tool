# -*- coding: utf-8 -*-
import re
import sys
import io

# Set UTF-8 encoding for output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

test = "<|ref|>text<|/ref|><|det|>[[36, 25, 912, 185]]<|/det|>"

# Test pattern
pattern = r'<\|det\|>(\[\[.*?\]\])<\/\|det\|>'
match = re.search(pattern, test)

with open('simple_test_result.txt', 'w', encoding='utf-8') as f:
    f.write("Regex Test Result\n")
    f.write("=" * 50 + "\n")
    f.write(f"Pattern: {pattern}\n")
    f.write(f"Test string: {test}\n")
    f.write(f"Match: {match is not None}\n")
    if match:
        f.write(f"Matched: {match.group(1)}\n")
        f.write("SUCCESS!\n")
    else:
        f.write("FAILED!\n")

print("Test complete. Check simple_test_result.txt")

