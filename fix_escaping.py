def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    bad_str = r"u.scope_division.join(\', \') : \'ALL\'"
    good_str = r"u.scope_division.join(', ') : 'ALL'"
    
    content = content.replace(bad_str, good_str)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

fix_file('index_render.html')
fix_file('static/index.html')
