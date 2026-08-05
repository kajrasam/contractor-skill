import os
import re

target_dir = r"d:\Work\งานใหม่\อบรม\2026\Vibe Coding Workshop\Project\contractor-skill"
files_to_patch = [
    os.path.join(target_dir, "index_render.html"), 
    os.path.join(target_dir, "static", "index.html"),
    os.path.join(target_dir, "scratch_html.html")
]

for filepath in files_to_patch:
    if not os.path.exists(filepath):
        continue
        
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
        
    if "eData._inDbUsers = true;" not in content:
        content = re.sub(
            r"(if\s*\(\s*officialPos\s*\)\s*dbUsers\[id\]\.position\s*=\s*officialPos;)",
            r"\1\n                        eData._inDbUsers = true;",
            content
        )
        
    if "employeeData = employeeDataAll.filter(e => e._inDbUsers);" not in content:
        content = re.sub(
            r"(//\s*Rebuild filters to reflect new/updated data from database)",
            r"employeeData = employeeDataAll.filter(e => e._inDbUsers);\n                \1",
            content
        )
        
    content = content.replace("e.username === id || e.user_id === id)", "e.username === id || e.user_id === id || e.USER === id)")
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
        
print("Patched successfully!")
