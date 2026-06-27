import re
with open('static/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

start = html.find('<select id="radar-filter"')
print(html[max(0, start-200):min(len(html), start+400)])
