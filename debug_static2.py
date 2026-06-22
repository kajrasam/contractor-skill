with open('d:/Work/งานใหม่/อบรม/2026/Vibe Coding Workshop/Project/competency-system/static/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re
match = re.search(r'function buildFiltersUI\(\).*?emps\.forEach', html, re.DOTALL)
if match:
    print(match.group(0))
else:
    print('Not found')
