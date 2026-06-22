import re
with open('static/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

idx = html.find('function updateAllViews()')
print(html[idx:idx+800])
