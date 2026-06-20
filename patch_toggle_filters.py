import re

files = [
    'd:/Work/งานใหม่/อบรม/2026/Vibe Coding Workshop/Project/competency-system/static/index.html',
    'd:/Work/งานใหม่/อบรม/2026/Vibe Coding Workshop/Project/competency-system/index_render.html'
]

pattern = r"window\.toggleFilterMenu = function\(menuId\) \{[\s\S]*?\}\s*(?=\n\s*// ---)"

replacement = """window.toggleFilterMenu = function(menuId) {
            const allMenus = document.querySelectorAll('.filter-menu');
            let found = false;
            allMenus.forEach(el => {
                if(el.id === menuId) {
                    el.classList.toggle('hidden');
                    found = true;
                } else {
                    el.classList.add('hidden');
                }
            });
            // Fallback for dynamically added menus without the class
            if (!found) {
                const target = document.getElementById(menuId);
                if (target) {
                    target.classList.toggle('hidden');
                }
            }
        }"""

for file_path in files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # We can also just use an exact regex replace:
    content = re.sub(r"window\.toggleFilterMenu = function\(menuId\) \{.*?\n\s*\};?", replacement, content, flags=re.DOTALL)
    
    # Just to be sure, let's also do another simpler replace
    old_func = """        window.toggleFilterMenu = function(menuId) {
            const menus = ['job-group-menu', 'pos-dropdown-menu', 'comp-group-menu', 'comp-dropdown-menu', 'idp-pos-menu', 'idp-emp-menu', 'dash-job-group-menu', 'dash-pos-menu', 'analytic-job-group-menu', 'analytic-pos-menu', 'analytic-emp-menu', 'analytic-group-menu', 'analytic-skill-menu'];
            menus.forEach(m => {
                const el = document.getElementById(m);
                if(el) {
                    if(m === menuId) el.classList.toggle('hidden');
                    else el.classList.add('hidden');
                }
            });
        }"""
        
    content = content.replace(old_func, replacement)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

print(f"Patched {len(files)} files to fix filter dropdown.")
