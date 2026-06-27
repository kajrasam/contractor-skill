import re

def fix_admin_checks(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # The full admin check string
    full_check = "(currentUser.id === 'Admin' || currentUser.id.toLowerCase().includes('admin') || (currentUser.role && (currentUser.role === 'Admin' || currentUser.role === 'Super Admin')))"
    
    # Let's find specific lines where the old check is used
    # 1362
    content = content.replace(
        "if (currentUser.id === 'Admin') toggleContainer.classList.remove('hidden');",
        f"if ({full_check}) toggleContainer.classList.remove('hidden');"
    )
    
    # 1884 & 1970
    content = content.replace(
        "const isAdmin = currentUser.id === 'Admin';",
        f"const isAdmin = {full_check};"
    )
    
    # 2147
    content = content.replace(
        """function setupEvaluationTab() {
    if (currentUser.id === 'Admin') {""",
        f"""function setupEvaluationTab() {{
    if ({full_check}) {{"""
    )
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Patched {filepath}")

fix_admin_checks('static/index.html')
fix_admin_checks('index_render.html')
