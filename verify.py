import esprima
import re

with open('static/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

scripts = re.findall(r'<script>(.*?)</script>', html, re.DOTALL)
for i, s in enumerate(scripts):
    try:
        esprima.parseScript(s)
        print(f'Script {i} OK')
    except Exception as e:
        print(f'Script {i} ERROR:', e)
