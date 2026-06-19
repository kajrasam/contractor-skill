with open('build_frontend.py', 'r', encoding='utf-8') as f:
    content = f.read()

# find new_js = """ ... """
import re
match = re.search(r'new_js = """(.*?)"""', content, re.DOTALL)
if match:
    with open('temp.js', 'w', encoding='utf-8') as f:
        f.write(match.group(1))
    print("Extracted JS")
else:
    print("Could not extract")
