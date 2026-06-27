import re

def fix_admin_checks_2(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    full_check = "(currentUser.id === 'Admin' || currentUser.id.toLowerCase().includes('admin') || (currentUser.role && (currentUser.role === 'Admin' || currentUser.role === 'Super Admin')))"
    
    # Let's fix line 2147 specifically by searching for it
    pattern = r'(function\s+setupEvaluationTab\(\)\s*\{\s*)if\s*\(\s*currentUser\.id\s*===\s*\'Admin\'\s*\)\s*\{'
    
    def replacer(match):
        return match.group(1) + f"if ({full_check}) {{"
        
    content, count = re.subn(pattern, replacer, content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Patched {filepath}, count={count}")

fix_admin_checks_2('static/index.html')
fix_admin_checks_2('index_render.html')
