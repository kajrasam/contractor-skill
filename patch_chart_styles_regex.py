import re

def swap_formats(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Update Self Eva. (Change #fbbf24 to #9333ea, transparent background, dotted line)
    # The current self eva color is usually #fbbf24 and rgba(251, 191, 36, 0.2)
    # 2. Update Before (Change #9333ea to #fbbf24, yellow background, solid line)
    # The current before color is usually #9333ea and transparent background
    
    # Let's temporarily change Self Eva to a placeholder so we don't accidentally match it when modifying Before
    content = re.sub(r"(label:\s*'Self Eva\.',.*?borderColor:\s*)'#fbbf24'(.*?backgroundColor:\s*)'rgba\(251, 191, 36, 0.2\)'", r"\g<1>'SELFEVA_COLOR'\g<2>'SELFEVA_BG'", content)
    
    # Update Before to use Self Eva's old styling
    content = re.sub(r"(label:\s*'Before',.*?borderColor:\s*)'#9333ea'(.*?backgroundColor:\s*)'transparent',\s*borderDash:\s*\[2, 2\]", r"\g<1>'#fbbf24'\g<2>'rgba(251, 191, 36, 0.2)'", content)
    
    # Now replace the placeholder for Self Eva with Before's old styling
    content = content.replace("'SELFEVA_COLOR'", "'#9333ea'").replace("'SELFEVA_BG'", "'transparent', borderDash: [5, 5]")
    
    # Also handle the points if they have specific point colors
    # Self Eva points originally had #fbbf24
    # Before points originally had #9333ea
    
    # We do the same placeholder trick for points
    content = re.sub(r"(label:\s*'Self Eva\.',.*?pointBackgroundColor:\s*)'#fbbf24'(.*?pointHoverBorderColor:\s*)'#fbbf24'", r"\g<1>'SELFEVA_PT'\g<2>'SELFEVA_PT'", content)
    
    content = re.sub(r"(label:\s*'Before',.*?pointBackgroundColor:\s*)'#9333ea'(.*?pointHoverBorderColor:\s*)'#9333ea'", r"\g<1>'#fbbf24'\g<2>'#fbbf24'", content)
    
    content = content.replace("'SELFEVA_PT'", "'#9333ea'")
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Regex Patched {filepath}")

import os
if os.path.exists('static/index.html'): swap_formats('static/index.html')
if os.path.exists('index_render.html'): swap_formats('index_render.html')
