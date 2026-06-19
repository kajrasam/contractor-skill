import re

html_path = 'd:\\Work\\งานใหม่\\อบรม\\2026\\Vibe Coding Workshop\\Project\\competency_system_dynamic_rbac_hierarchy.html'

with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find the thead of employee data table
start_str = '<tr class="bg-slate-50 text-slate-600 font-bold border-b border-slate-200 text-xs uppercase tracking-wider">'
end_str = '</tr>'

# We need to find the specific block. It's around line 719.
# Let's just search for it using regex that matches the block exactly.
pattern = r'(<tr class="bg-slate-50 text-slate-600 font-bold border-b border-slate-200 text-xs uppercase tracking-wider">)(.*?)(</tr>\s*</thead>\s*<tbody id="employee-data-tbody")'

match = re.search(pattern, content, re.DOTALL)
if match:
    thead_content = match.group(2)
    
    # For each <th ...>Text</th>, inject <br><input ...>
    # Wait, some th have text inside like <th ...>Name (TH)</th>
    # Some have classes.
    def replacer(m):
        th_start = m.group(1)
        th_text = m.group(2)
        # Add align-top to th_start if not present, but it's easier to just inject input
        # Let's add align-top to th classes
        if 'class="' in th_start:
            th_start = th_start.replace('class="', 'class="align-top ')
        
        input_html = f'<input type="text" class="emp-filter-input w-full mt-2 px-2 py-1 border border-slate-200 rounded text-xs font-normal text-slate-700 outline-none focus:border-scg-500 placeholder-slate-300 normal-case" placeholder="Search..." onkeyup="filterEmployeeTable()">'
        return f'{th_start}<div class="mb-1">{th_text}</div>{input_html}</th>'

    new_thead = re.sub(r'(<th[^>]*>)(.*?)(</th>)', replacer, thead_content, flags=re.DOTALL)
    
    new_content = content[:match.start()] + match.group(1) + new_thead + match.group(3) + content[match.end():]
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Injected filters into HTML.")
else:
    print("Could not find thead block.")
