import re
import os

files_to_process = [
    'd:\\Work\\งานใหม่\\อบรม\\2026\\Vibe Coding Workshop\\Project\\competency-system\\static\\index.html',
    'd:\\Work\\งานใหม่\\อบรม\\2026\\Vibe Coding Workshop\\Project\\competency-system\\index_render.html'
]

for filepath in files_to_process:
    if not os.path.exists(filepath):
        continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Line 1734ish (updateEvalUI)
    # const subs = actingAsRole === 'Admin' ? [] : getSubordinates(actingAsRole);
    # Actually, we should filter it after it's defined:
    # const subs = applyGlobalFiltersToSubIds(actingAsRole === 'Admin' ? [] : getSubordinates(actingAsRole));
    # Wait, if Admin has [], then Admin sees nothing. Actually `subs` is for who they can evaluate.
    content = content.replace(
        "const subs = actingAsRole === 'Admin' ? [] : getSubordinates(actingAsRole);",
        "const subs = applyGlobalFiltersToSubIds(actingAsRole === 'Admin' ? [] : getSubordinates(actingAsRole));"
    )

    # 2. Line 1932ish (buildDashboard)
    # let subs = getSubordinates(currentUserId);
    content = content.replace(
        "let subs = getSubordinates(currentUserId);",
        "let subs = applyGlobalFiltersToSubIds(getSubordinates(currentUserId));"
    )

    # 3. Line 1979ish (buildIDP)
    # let visibleUsers = currentUser.id === 'Admin' ? Object.keys(dbUsers).filter(id => id !== 'Admin') : [currentUser.id, ...getSubordinates(currentUser.id)];
    content = content.replace(
        "let visibleUsers = currentUser.id === 'Admin' ? Object.keys(dbUsers).filter(id => id !== 'Admin') : [currentUser.id, ...getSubordinates(currentUser.id)];",
        "let visibleUsers = applyGlobalFiltersToSubIds(currentUser.id === 'Admin' ? Object.keys(dbUsers).filter(id => id !== 'Admin') : [currentUser.id, ...getSubordinates(currentUser.id)]);"
    )

    # 4. Line 2431ish (buildAnalytic)
    # visibleUsers = [currentUser.id, ...getSubordinates(currentUser.id)];
    # Wait, what if it's admin?
    content = content.replace(
        "visibleUsers = [currentUser.id, ...getSubordinates(currentUser.id)];",
        "visibleUsers = applyGlobalFiltersToSubIds([currentUser.id, ...getSubordinates(currentUser.id)]);"
    )
    # Also for Admin in buildAnalytic:
    # visibleUsers = Object.keys(dbUsers).filter(id => id !== 'Admin');
    content = content.replace(
        "visibleUsers = Object.keys(dbUsers).filter(id => id !== 'Admin');",
        "visibleUsers = applyGlobalFiltersToSubIds(Object.keys(dbUsers).filter(id => id !== 'Admin'));"
    )

    # Note: If admin sees everything, we apply the global filter to them too.

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Updated variable assignments in {os.path.basename(filepath)}")
