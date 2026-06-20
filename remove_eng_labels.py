import re

files = [
    'd:/Work/งานใหม่/อบรม/2026/Vibe Coding Workshop/Project/competency-system/static/index.html',
    'd:/Work/งานใหม่/อบรม/2026/Vibe Coding Workshop/Project/competency-system/index_render.html'
]

for file_path in files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace "กรองตามกลุ่มงาน (Job Groups)" with "กรองตามกลุ่มงาน"
    content = content.replace('กรองตามกลุ่มงาน (Job Groups)', 'กรองตามกลุ่มงาน')
    
    # Replace "กรองตามตำแหน่ง (Position Name)" with "กรองตามตำแหน่ง"
    content = content.replace('กรองตามตำแหน่ง (Position Name)', 'กรองตามตำแหน่ง')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

print(f"Removed English text from filter labels in {len(files)} files.")
