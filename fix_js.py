with open('build_frontend.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(len(lines)):
    # Fix the BOM line which has an actual newline embedded if it was broken, but wait, it might just be the literal BOM
    if 'let csvContent = "\\ufeff"' in lines[i] or 'let csvContent = "\\uFEFF"' in lines[i]:
        pass
    if 'let csvContent =' in lines[i] and 'headers.join' in lines[i]:
        lines[i] = '            let csvContent = "\\\\uFEFF" + headers.join(",") + "\\\\n";\n'
    if 'csvContent += row.join' in lines[i]:
        lines[i] = '                csvContent += row.join(",") + "\\\\n";\n'

with open('build_frontend.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)
