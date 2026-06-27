for fname in ['index_render.html', 'static/index.html']:
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
    if '</div>;\n                    \n                    const beforeVal' in content:
        content = content.replace('</div>;\n                    \n                    const beforeVal', '</div>`;\n                    \n                    const beforeVal')
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'{fname} fixed again!')
