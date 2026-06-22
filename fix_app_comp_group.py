import re

with open('d:/Work/งานใหม่/อบรม/2026/Vibe Coding Workshop/Project/competency-system/app.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('competencies.append({"name": c["name"], "group": c["group"]})', 'competencies.append({"name": c["name"], "group": c.get("competency_group", c.get("group", ""))})')

with open('d:/Work/งานใหม่/อบรม/2026/Vibe Coding Workshop/Project/competency-system/app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("app.py fixed competencies group key")
