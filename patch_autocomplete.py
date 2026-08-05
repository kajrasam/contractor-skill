import re

def add_autocomplete_off(fp):
    with open(fp, 'r', encoding='utf-8') as f:
        c = f.read()

    # Add autocomplete="off" to add-shift, add-position, add-level
    c = c.replace('id="add-shift" list=', 'id="add-shift" autocomplete="off" list=')
    c = c.replace('id="add-position" list=', 'id="add-position" autocomplete="off" list=')
    c = c.replace('id="add-level" list=', 'id="add-level" autocomplete="off" list=')

    with open(fp, 'w', encoding='utf-8') as f:
        f.write(c)

for fp in ['index_render.html', 'static/index.html']:
    add_autocomplete_off(fp)

print("Added autocomplete=off")
