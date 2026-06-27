import re
with open('static/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

start = html.find('dashboard-radar-')
if start == -1:
    print('No dashboard-radar- found')
else:
    print(html[max(0, start-500):min(len(html), start+500)])
