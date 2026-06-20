import re

files = [
    'd:/Work/งานใหม่/อบรม/2026/Vibe Coding Workshop/Project/competency-system/static/index.html',
    'd:/Work/งานใหม่/อบรม/2026/Vibe Coding Workshop/Project/competency-system/index_render.html'
]

old_text = 'ผูก Competency ในตำแหน่งนี้ ก่อน'
new_text = 'กรุณาผูก Competency ในตำแหน่งนี้ ก่อน'

for file_path in files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace the text
    content = content.replace(old_text, new_text)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

print(f"Updated text in {len(files)} files.")
