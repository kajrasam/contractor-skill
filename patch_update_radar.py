import re

def fix_update_radar_filter(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # The current code in updateRadarFilter is:
    # if (type === 'idp') { if (typeof renderIDPContent === 'function') renderIDPContent(); }
    
    better_idp_update = """if (type === 'idp') {
                let visibleUsers = [];
                if (currentUser.id === 'Admin' || currentUser.id.toLowerCase().includes('admin') || (currentUser.role && (currentUser.role === 'Admin' || currentUser.role === 'Super Admin'))) {
                    visibleUsers = applyGlobalFiltersToSubIds(Object.keys(dbUsers).filter(uid => uid !== 'Admin'));
                } else {
                    visibleUsers = applyGlobalFiltersToSubIds([currentUser.id, ...getSubordinates(currentUser.id)]);
                }
                if (visibleUsers.length === 1) {
                    const empId = visibleUsers[0];
                    const emp = dbUsers[empId];
                    const targets = positionTargets[emp.position] || [];
                    drawIDPRadar(emp, targets);
                } else {
                    if (typeof renderIDPContent === 'function') renderIDPContent();
                }
            }"""
            
    content = content.replace(
        "if (type === 'idp') { if (typeof renderIDPContent === 'function') renderIDPContent(); }",
        better_idp_update
    )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Patched {filepath}")

fix_update_radar_filter('static/index.html')
fix_update_radar_filter('index_render.html')
