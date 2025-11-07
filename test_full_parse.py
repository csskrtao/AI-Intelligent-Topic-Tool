# -*- coding: utf-8 -*-
import re
import json

test_content = """<|ref|>text<|/ref|><|det|>[[36, 25, 912, 185]]<|/det|>       
42.(10分)现有题目
<|ref|>text<|/ref|><|det|>[[67, 194, 914, 345]]<|/det|>      
（1）设计一个算法"""

blocks = []
lines = test_content.split('\n')
current_box = None
current_text_lines = []

debug_output = []
debug_output.append(f"Total lines: {len(lines)}\n")

for i, line in enumerate(lines):
    debug_output.append(f"Line {i}: {repr(line)}\n")
    det_match = re.search(r'<\|det\|>(\[\[.*?\]\])<\/\|det\|>', line)
    debug_output.append(f"  Match: {det_match is not None}\n")
    
    if det_match:
        # Save previous block
        if current_box is not None and current_text_lines:
            text = '\n'.join(current_text_lines).strip()
            if text:
                blocks.append({'text': text, 'box': current_box})
        
        # Parse coordinates
        try:
            coords_str = det_match.group(1)
            coords = json.loads(coords_str)
            if coords and len(coords) > 0 and len(coords[0]) == 4:
                current_box = coords[0]
            else:
                current_box = [0, 0, 0, 0]
        except:
            current_box = [0, 0, 0, 0]
        
        # Reset text lines
        current_text_lines = []
        
        # Extract text after tags
        text_after_tag = re.sub(r'<\|ref\|>.*?<\/\|ref\|>', '', line)
        text_after_tag = re.sub(r'<\|det\|>.*?<\/\|det\|>', '', text_after_tag)
        text_after_tag = text_after_tag.strip()
        if text_after_tag:
            current_text_lines.append(text_after_tag)
    else:
        # Regular text line
        clean_line = re.sub(r'<\|ref\|>.*?<\/\|ref\|>', '', line)
        clean_line = clean_line.strip()
        if clean_line:
            current_text_lines.append(clean_line)

# Save last block
if current_box is not None and current_text_lines:
    text = '\n'.join(current_text_lines).strip()
    if text:
        blocks.append({'text': text, 'box': current_box})

with open('full_parse_result.txt', 'w', encoding='utf-8') as f:
    f.write("Full Parse Test\n")
    f.write("=" * 60 + "\n")

    f.write("DEBUG OUTPUT:\n")
    f.write("-" * 60 + "\n")
    for line in debug_output:
        f.write(line)
    f.write("\n")

    f.write("RESULTS:\n")
    f.write("-" * 60 + "\n")
    f.write(f"Parsed {len(blocks)} blocks\n\n")

    for i, block in enumerate(blocks, 1):
        f.write(f"Block {i}:\n")
        f.write(f"  Box: {block['box']}\n")
        f.write(f"  Text: {block['text']}\n\n")

print(f"Parsed {len(blocks)} blocks. Check full_parse_result.txt")

