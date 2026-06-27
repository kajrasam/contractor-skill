import re
with open('static/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

start = html.find('function renderDashboard')
if start == -1:
    print('No renderDashboard found')
else:
    print(html[max(0, start):min(len(html), start+1500)])
