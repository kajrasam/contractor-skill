with open('static/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

idx = html.find('id="global-filters-container"')
print('Location:', idx)
print(html[idx-200:idx+200])
