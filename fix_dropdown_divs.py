import re

def fix_dropdown_divs(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Fix Analytic dropdown div
    content = content.replace(
        '<div class="analytic-radar-cb absolute top-full left-0 right-0 mt-1 bg-white border border-slate-100 rounded-lg shadow-xl z-[60] hidden p-2">',
        '<div id="analytic-radar-filter-dropdown" class="absolute top-full left-0 right-0 mt-1 bg-white border border-slate-100 rounded-lg shadow-xl z-[60] hidden p-2">'
    )
    
    # 2. Fix IDP dropdown div
    content = content.replace(
        '<div class="idp-radar-cb absolute top-full left-0 right-0 mt-1 bg-white border border-slate-100 rounded-lg shadow-xl z-[60] hidden p-2">',
        '<div id="idp-radar-filter-dropdown" class="absolute top-full left-0 right-0 mt-1 bg-white border border-slate-100 rounded-lg shadow-xl z-[60] hidden p-2">'
    )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Patched dropdown divs in {filepath}")

fix_dropdown_divs('static/index.html')
fix_dropdown_divs('index_render.html')
