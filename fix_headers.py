import re

files = [
    'd:/Work/งานใหม่/อบรม/2026/Vibe Coding Workshop/Project/competency-system/static/index.html',
    'd:/Work/งานใหม่/อบรม/2026/Vibe Coding Workshop/Project/competency-system/index_render.html'
]

for file_path in files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove headers (case insensitive)
    content = re.sub(r'<th[^>]*>(?i)Retirement Year</th>\s*', '', content)
    content = re.sub(r'<th[^>]*>(?i)อายุงาน</th>\s*', '', content)
    content = re.sub(r'<th[^>]*>(?i)Age</th>\s*', '', content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

print("Fixed headers")
