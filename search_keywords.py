import json

def search(filepath, keyword):
    results = []
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if keyword.lower() in line.lower():
                results.append(f"{i}: {line.strip()}")
    return results

res1 = search('static/index.html', 'completed skill level')
res2 = search('static/index.html', 'readiness')
res3 = search('static/index.html', 'ความพร้อมโดยรวม')

with open('search_result.txt', 'w', encoding='utf-8') as f:
    f.write("COMPLETED SKILL LEVEL:\n")
    f.write("\n".join(res1))
    f.write("\n\nREADINESS:\n")
    f.write("\n".join(res2))
    f.write("\n\nความพร้อมโดยรวม:\n")
    f.write("\n".join(res3))
