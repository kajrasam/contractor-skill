import re
with open('d:/Work/งานใหม่/อบรม/2026/Vibe Coding Workshop/Project/competency-system/index_render.html', 'r', encoding='utf-8') as f:
    html = f.read()

matches = re.findall(r'<section id=".*?"', html)
for m in matches:
    print(m)
