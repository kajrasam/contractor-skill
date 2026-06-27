import re

def fix_idp_checkboxes(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the filter dropdown block in renderIDPContent
    # Make sure we don't accidentally match something else.
    # The dropdown contains <div id="idp-radar-filter-dropdown" ...
    pattern = r'(<div id="idp-radar-filter-dropdown" class="absolute top-full left-0 right-0 mt-1 bg-white border border-slate-100 rounded-lg shadow-xl z-\[60\] hidden p-2">)(.*?)(</div>\s*</div>\s*</div>)'
    
    # We will replace the entire inner part of the dropdown
    def replacer(match):
        pre_html = match.group(1)
        return pre_html + \
               """
                                        <label class="flex items-center gap-2 p-1.5 hover:bg-slate-50 rounded cursor-pointer text-xs">
                                            <input type="checkbox" ${activeFiltersIDP.includes('target') ? 'checked' : ''} value="target" onchange="updateRadarFilter('idp')" class="idp-radar-cb w-3.5 h-3.5 rounded text-scg-600 border-slate-300 focus:ring-scg-500"> Target
                                        </label>
                                        <label class="flex items-center gap-2 p-1.5 hover:bg-slate-50 rounded cursor-pointer text-xs">
                                            <input type="checkbox" ${activeFiltersIDP.includes('before') ? 'checked' : ''} value="before" onchange="updateRadarFilter('idp')" class="idp-radar-cb w-3.5 h-3.5 rounded text-purple-500 border-slate-300 focus:ring-purple-500"> Before
                                        </label>
                                        <label class="flex items-center gap-2 p-1.5 hover:bg-slate-50 rounded cursor-pointer text-xs">
                                            <input type="checkbox" ${activeFiltersIDP.includes('self') ? 'checked' : ''} value="self" onchange="updateRadarFilter('idp')" class="idp-radar-cb w-3.5 h-3.5 rounded text-amber-500 border-slate-300 focus:ring-amber-500"> Self Eva.
                                        </label>
                                        <label class="flex items-center gap-2 p-1.5 hover:bg-slate-50 rounded cursor-pointer text-xs">
                                            <input type="checkbox" ${activeFiltersIDP.includes('actual') ? 'checked' : ''} value="actual" onchange="updateRadarFilter('idp')" class="idp-radar-cb w-3.5 h-3.5 rounded text-red-600 border-slate-300 focus:ring-red-600"> Actual
                                        </label>
""" + match.group(3)
               
    content, count = re.subn(pattern, replacer, content, flags=re.DOTALL)
    
    insert_pattern = r'(container\.innerHTML = `\s*<!-- IDP Header Section -->)'
    content, count_insert = re.subn(insert_pattern, r'const activeFiltersIDP = activeRadarFilters["idp"] || ["target", "self", "before", "actual"];\n            \1', content)
    
    # Fix the text to show active filters correctly
    text_logic = """${activeFiltersIDP.length === 4 ? 'แสดงทั้งหมด' : (activeFiltersIDP.length === 0 ? 'ซ่อนทั้งหมด' : activeFiltersIDP.map(v => ({'target': 'Target', 'self': 'Self', 'before': 'Before', 'actual': 'Actual'})[v]).join(', '))}"""
    
    # In index.html, it's currently `<span id="idp-radar-filter-text" class="text-slate-600">แสดงทั้งหมด</span>`
    # Let's replace it robustly:
    content = re.sub(
        r'<span id="idp-radar-filter-text" class="text-slate-600">.*?</span>',
        f'<span id="idp-radar-filter-text" class="text-slate-600">{text_logic}</span>',
        content
    )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Patched {filepath}, count={count}, count_insert={count_insert}")

fix_idp_checkboxes('static/index.html')
fix_idp_checkboxes('index_render.html')
