with open('static/index.html', 'r', encoding='utf-8') as f:
    html = f.read()
start = html.find('id="analytic-content"')
print(html[max(0, start):min(len(html), start+1500)])
