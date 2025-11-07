# -*- coding: utf-8 -*-
import re

# Exact test string from debug output
test = '<|ref|>text<|/ref|><|det|>[[36, 25, 912, 185]]<|/det|>       '

patterns = [
    r'<\|det\|>',
    r'<\/\|det\|>',
    r'<\|/det\|>',
    r'<[|]/det[|]>',
    r'<\|det\|>.*?<\/\|det\|>',
    r'<\|det\|>.*?<\|/det\|>',
]

with open('exact_regex_output.txt', 'w', encoding='utf-8') as f:
    f.write("Testing exact regex patterns\n")
    f.write("=" * 60 + "\n")
    f.write(f"Test string: {test}\n\n")
    
    for pattern in patterns:
        match = re.search(pattern, test)
        f.write(f"Pattern: {pattern}\n")
        f.write(f"  Match: {match is not None}\n")
        if match:
            f.write(f"  Matched: {match.group(0)}\n")
        f.write("\n")

print("Check exact_regex_output.txt")

