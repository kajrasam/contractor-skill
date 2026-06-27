import re
with open('static/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'id="tab-admin"' in line:
        for j in range(i, i+5):
            print(f'{j}: {lines[j].strip()}')
        break
