import os

def patch_file(filepath):
    if not os.path.exists(filepath):
        return
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    # Change 1: Call buildFiltersUI() at the end of fetchInitialData
    target1 = """                        if (officialPos) dbUsers[id].position = officialPos;
                    }
                });
                if (!silent) {"""
    
    replacement1 = """                        if (officialPos) dbUsers[id].position = officialPos;
                    }
                });
                
                // Rebuild filters to reflect new/updated data from database
                setTimeout(() => { if(typeof buildFiltersUI === 'function') buildFiltersUI(); }, 0);
                
                if (!silent) {"""
    
    # Change 2: Make buildFiltersUI use employeeDataAll for ALL tabs
    target2 = "const dataSource = (tabId === 'admin') ? employeeDataAll : employeeData;"
    replacement2 = "const dataSource = employeeDataAll; // Use all DB data for filters across all tabs as requested"

    patched = False
    
    if target1 in html:
        html = html.replace(target1, replacement1)
        patched = True
    else:
        print(f"Target 1 not found in {filepath}")

    if target2 in html:
        html = html.replace(target2, replacement2)
        patched = True
    else:
        print(f"Target 2 not found in {filepath}")

    if patched:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"Patched {filepath}")

patch_file('index_render.html')
patch_file('static/index.html')
