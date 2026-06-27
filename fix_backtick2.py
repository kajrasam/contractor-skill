import os

for fname in ['index_render.html', 'static/index.html']:
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if '</div>`;`;' in content:
        content = content.replace('</div>`;`;', '</div>`;')
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'{fname} fixed `;;!')
    else:
        print(f'{fname} NO `;; FOUND!')
