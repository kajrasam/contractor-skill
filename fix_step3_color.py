import re

files = [
    'd:/Work/งานใหม่/อบรม/2026/Vibe Coding Workshop/Project/competency-system/static/index.html',
    'd:/Work/งานใหม่/อบรม/2026/Vibe Coding Workshop/Project/competency-system/index_render.html'
]

old_class_left = 'bg-scg-50 text-scg-600 flex items-center justify-center font-bold shrink-0 border-4 border-white shadow-sm z-10">3</div>'
new_class = 'bg-scg-800 text-white flex items-center justify-center font-bold shrink-0 border-4 border-white shadow-md z-10">3</div>'

for file_path in files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace the left one to match the right one
    content = content.replace(old_class_left, new_class)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

print(f"Fixed step 3 colors in {len(files)} files.")
