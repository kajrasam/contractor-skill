import re

files = [
    'd:/Work/งานใหม่/อบรม/2026/Vibe Coding Workshop/Project/competency-system/static/index.html',
    'd:/Work/งานใหม่/อบรม/2026/Vibe Coding Workshop/Project/competency-system/index_render.html'
]

old_setup = """        function setupDashboardTab() {
            
            const currentUserId = currentUser.id;
            let subs = applyGlobalFiltersToSubIds(getSubordinates(currentUserId));
            let toShow = [];

            if (currentUserId === 'Admin') {
                toShow = Object.keys(dbUsers).filter(id => id !== 'Admin');
                document.getElementById('dash-manager-view').style.display = 'block';
            } else if (subs.length === 0) {
                toShow = [currentUserId];
                document.getElementById('dash-manager-view').style.display = 'none';
            } else {
                toShow = subs;
                document.getElementById('dash-manager-view').style.display = 'block';
            }"""

new_setup = """        function setupDashboardTab() {
            
            const currentUserId = currentUser.id;
            const mySubs = getSubordinates(currentUserId);
            let toShow = [];

            if (currentUserId === 'Admin') {
                toShow = applyGlobalFiltersToSubIds(Object.keys(dbUsers).filter(id => id !== 'Admin'));
                document.getElementById('dash-manager-view').style.display = 'block';
            } else if (mySubs.length === 0) {
                toShow = applyGlobalFiltersToSubIds([currentUserId]);
                document.getElementById('dash-manager-view').style.display = 'none';
            } else {
                toShow = applyGlobalFiltersToSubIds(mySubs);
                document.getElementById('dash-manager-view').style.display = 'block';
            }"""

for file_path in files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    content = content.replace(old_setup, new_setup)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

print(f"Patched {len(files)} files to apply dashboard filters.")
