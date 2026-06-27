with open('static/index.html', 'r', encoding='utf-8') as f:
    html = f.read()
start = html.find('id="tab-analytic"')
print(html[start:start+1000])
