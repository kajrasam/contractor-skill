import os

def patch_file(filepath):
    if not os.path.exists(filepath):
        return
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    target = "pk_field: e.PersonID ? 'PersonID' : (e.id ? 'id' : 'person_id'),\n                    pk_value: e.PersonID || e.id || e.person_id,"
    replacement = "pk_field: e.id ? 'id' : (e.PersonID ? 'PersonID' : 'person_id'),\n                    pk_value: e.id || e.PersonID || e.person_id,"

    if target in html:
        html = html.replace(target, replacement)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"Patched {filepath}")
    else:
        print(f"Target not found in {filepath}")

patch_file('index_render.html')
patch_file('static/index.html')
