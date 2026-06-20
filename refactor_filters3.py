import os
files = ['d:\\Work\\งานใหม่\\อบรม\\2026\\Vibe Coding Workshop\\Project\\competency-system\\static\\index.html', 'd:\\Work\\งานใหม่\\อบรม\\2026\\Vibe Coding Workshop\\Project\\competency-system\\index_render.html']
for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    content = content.replace("visibleUsers = Object.keys(dbUsers).filter(uid => uid !== 'Admin');", "visibleUsers = applyGlobalFiltersToSubIds(Object.keys(dbUsers).filter(uid => uid !== 'Admin'));")
    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)
