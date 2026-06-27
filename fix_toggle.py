import os

injection = """            document.getElementById('sliders-container').innerHTML = html;
            
            const evalModeToggle = document.getElementById('eval-mode-toggle');
            if (evalModeToggle) {
                if (currentUser.id === id) {
                    evalModeToggle.classList.add('hidden');
                } else {
                    evalModeToggle.classList.remove('hidden');
                    const actualRadio = document.querySelector('input[name="evalModeToggle"][value="actual"]');
                    if (actualRadio) actualRadio.checked = true;
                    if (typeof toggleEvalViewMode === 'function') {
                        toggleEvalViewMode('actual');
                    }
                }
            }"""

for fname in ['index_render.html', 'static/index.html']:
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if "const evalModeToggle = document.getElementById('eval-mode-toggle');" not in content:
        content = content.replace("            document.getElementById('sliders-container').innerHTML = html;", injection)
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'{fname} fixed!')
    else:
        print(f'{fname} already has the logic!')
