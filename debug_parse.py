# -*- coding: utf-8 -*-
import re
import json

test_content = """<|ref|>text<|/ref|><|det|>[[36, 25, 912, 185]]<|/det|>       
42.(10分)现有题目"""

print("Debug Parse")
print("=" * 60)
print(f"Test content:\n{repr(test_content)}\n")

blocks = []
lines = test_content.split('\n')
current_box = None
current_text_lines = []

print(f"Total lines: {len(lines)}\n")

for i, line in enumerate(lines):
    print(f"Line {i}: {repr(line)}")
    
    # Check for det tag
    det_match = re.search(r'<\|det\|>(\[\[.*?\]\])<\/\|det\|>', line)
    print(f"  det_match: {det_match is not None}")
    
    if det_match:
        print(f"  Matched coords: {det_match.group(1)}")
        
        # Save previous block
        print(f"  current_box before: {current_box}")
        print(f"  current_text_lines before: {current_text_lines}")
        
        if current_box is not None and current_text_lines:
            text = '\n'.join(current_text_lines).strip()
            if text:
                print(f"  Saving block: box={current_box}, text={text[:30]}...")
                blocks.append({'text': text, 'box': current_box})
        
        # Parse new coordinates
        try:
            coords_str = det_match.group(1)
            coords = json.loads(coords_str)
            print(f"  Parsed coords: {coords}")
            if coords and len(coords) > 0 and len(coords[0]) == 4:
                current_box = coords[0]
                print(f"  Set current_box to: {current_box}")
            else:
                current_box = [0, 0, 0, 0]
        except Exception as e:
            print(f"  Error parsing coords: {e}")
            current_box = [0, 0, 0, 0]
        
        # Reset text lines
        current_text_lines = []
        
        # Extract text after tags
        text_after_tag = re.sub(r'<\|ref\|>.*?<\/\|ref\|>', '', line)
        text_after_tag = re.sub(r'<\|det\|>.*?<\/\|det\|>', '', text_after_tag)
        text_after_tag = text_after_tag.strip()
        print(f"  text_after_tag: {repr(text_after_tag)}")
        if text_after_tag:
            current_text_lines.append(text_after_tag)
            print(f"  Added to current_text_lines")
    else:
        # Regular text line
        clean_line = re.sub(r'<\|ref\|>.*?<\/\|ref\|>', '', line)
        clean_line = clean_line.strip()
        print(f"  clean_line: {repr(clean_line)}")
        if clean_line:
            current_text_lines.append(clean_line)
            print(f"  Added to current_text_lines")
    
    print()

# Save last block
print("Saving last block...")
print(f"  current_box: {current_box}")
print(f"  current_text_lines: {current_text_lines}")

if current_box is not None and current_text_lines:
    text = '\n'.join(current_text_lines).strip()
    if text:
        print(f"  Saving: box={current_box}, text={text}")
        blocks.append({'text': text, 'box': current_box})

print()
print("=" * 60)
print(f"Total blocks: {len(blocks)}")
for i, block in enumerate(blocks, 1):
    print(f"Block {i}: box={block['box']}, text={block['text']}")

