with open('static/index.html', 'r', encoding='utf-8') as f:
    html = f.read()
start = html.find('<canvas id="analyticRadarChart"')
print(html[max(0, start-1000):min(len(html), start+100)])
