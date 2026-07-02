import os

def patch_file(filepath):
    if not os.path.exists(filepath):
        return
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    target = """function buildFiltersUI(tabId = null) {"""
    replacement = """function buildFiltersUI(tabId = null) {
            if (!currentUser) return;"""

    if target in html and replacement not in html:
        html = html.replace(target, replacement)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"Patched {filepath}")
    else:
        print(f"Target not found or already patched in {filepath}")

patch_file('index_render.html')
patch_file('static/index.html')
