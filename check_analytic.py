with open('static/index.html', 'r', encoding='utf-8') as f:
    html = f.read()
start = html.find('analyticRadarChart')
print(html[max(0, start-800):min(len(html), start+100)])
