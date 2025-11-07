# -*- coding: utf-8 -*-
import re

test = "<|det|>[[36, 25, 912, 185]]<|/det|>"

patterns = [
    (r'<\|det\|>', 'Escaped pipe with backslash'),
    (r'<[|]det[|]>', 'Pipe in character class'),
    (r'<\|det\|>.*?<\|/det\|>', 'Full pattern with backslash'),
    (r'<[|]det[|]>.*?<[|]/det[|]>', 'Full pattern with character class'),
]

with open('pipe_test_result.txt', 'w', encoding='utf-8') as f:
    f.write("Testing different pipe escape methods\n")
    f.write("=" * 60 + "\n")
    f.write(f"Test string: {test}\n\n")
    
    for pattern, desc in patterns:
        match = re.search(pattern, test)
        f.write(f"{desc}:\n")
        f.write(f"  Pattern: {pattern}\n")
        f.write(f"  Match: {match is not None}\n")
        if match:
            f.write(f"  Matched: {match.group(0)}\n")
        f.write("\n")

print("Test complete. Check pipe_test_result.txt")

