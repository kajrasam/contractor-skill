import sys
with open('build_frontend.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace physical newline syntax inside python string literal
# Notice that the literal python string "\n" was rendered as actual newline in JS.
# We need to render it as literally "\n" in JS, which means in python we write "\\n"
content = content.replace('let csvContent = "\\uFEFF" + headers.join(",") + "\\n";', 'let csvContent = "\\\\uFEFF" + headers.join(",") + "\\\\n";')
content = content.replace('csvContent += row.join(",") + "\\n";', 'csvContent += row.join(",") + "\\\\n";')

with open('build_frontend.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("Fixed!")
