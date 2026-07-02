import os

def patch_file(filepath):
    if not os.path.exists(filepath):
        return
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    target = "body: JSON.stringify({ userId: currentUser })"
    replacement = "body: JSON.stringify({ userId: currentUser.id })"

    if target in html:
        html = html.replace(target, replacement)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"Patched {filepath}")
    else:
        print(f"Target not found in {filepath}")

patch_file('index_render.html')
patch_file('static/index.html')
