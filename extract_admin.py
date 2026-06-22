with open('static/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

idx = html.find('id="tab-admin"')
if idx != -1:
    print(html[idx-50:idx+1500])
else:
    print("Not found tab-admin")
