with open('d:/Work/งานใหม่/อบรม/2026/Vibe Coding Workshop/Project/competency-system/static/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re
match = re.search(r'id="job-group-filters"', html)
if match:
    print('Found job-group-filters in static/index.html')
else:
    print('Not found')
