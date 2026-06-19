import re

html_path = 'd:\\Work\\งานใหม่\\อบรม\\2026\\Vibe Coding Workshop\\Project\\competency_system_dynamic_rbac_hierarchy.html'

with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# We want to remove: <div class="mb-1">Text</div><input type="text" class="emp-filter-input ...">
# and just leave the Text.
# Pattern matches <th ...><div class="mb-1">(.*?)</div><input[^>]*></th>
def replacer(m):
    th_start = m.group(1)
    text = m.group(2)
    return f'{th_start}{text}</th>'

# Find the thead section
pattern = r'(<tr class="bg-slate-50 text-slate-600 font-bold border-b border-slate-200 text-xs uppercase tracking-wider">)(.*?)(</tr>)'
match = re.search(pattern, content, re.DOTALL)

if match:
    thead_content = match.group(2)
    # The current thead_content has things like <th class="..."> <div class="mb-1">Person ID</div><input ...> </th>
    # Let's replace the inner part
    new_thead = re.sub(r'(<th[^>]*>)\s*<div class="mb-1">(.*?)</div>\s*<input[^>]*>\s*(</th>)', replacer, thead_content, flags=re.DOTALL)
    
    new_content = content[:match.start()] + match.group(1) + new_thead + match.group(3) + content[match.end():]
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Reverted filters in HTML.")
else:
    print("Could not find thead block.")
