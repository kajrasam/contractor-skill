import re

def patch_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    # Replace trainingMatrix with positionTargets in hasCompetencyFilterMatch
    html = html.replace('!trainingMatrix[posName]', '!positionTargets[posName]')
    html = html.replace('const targets = trainingMatrix[posName];', 'const targets = positionTargets[posName];')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Patched {filepath}")

patch_file('static/index.html')
patch_file('index_render.html')
