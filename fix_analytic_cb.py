import re

def fix_analytic_checkboxes(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the filter dropdown block in Analytic Tab
    pattern = r'(<div class="w-full sm:w-64">.*?<label class="block text-\[10px\] font-bold text-slate-500 mb-1">แสดงข้อมูล \(Filter\)</label>.*?<div id="analytic-radar-filter-dropdown".*?>\s*)(.*?)(</div>\s*</div>\s*</div>)'
    
    def replacer(match):
        pre_html = match.group(1)
        # We rewrite the checkboxes cleanly without analytic-radar-cb on the label.
        return pre_html + \
               """<label class="flex items-center gap-2 p-1.5 hover:bg-slate-50 rounded cursor-pointer text-xs">
                                    <input type="checkbox" checked value="target" onchange="updateRadarFilter('analytic')" class="analytic-radar-cb w-3.5 h-3.5 rounded text-scg-600 border-slate-300 focus:ring-scg-500"> Target
                                </label>
                                <label class="flex items-center gap-2 p-1.5 hover:bg-slate-50 rounded cursor-pointer text-xs">
                                    <input type="checkbox" checked value="before" onchange="updateRadarFilter('analytic')" class="analytic-radar-cb w-3.5 h-3.5 rounded text-purple-500 border-slate-300 focus:ring-purple-500"> Before
                                </label>
                                <label class="flex items-center gap-2 p-1.5 hover:bg-slate-50 rounded cursor-pointer text-xs">
                                    <input type="checkbox" checked value="self" onchange="updateRadarFilter('analytic')" class="analytic-radar-cb w-3.5 h-3.5 rounded text-amber-500 border-slate-300 focus:ring-amber-500"> Self Eva.
                                </label>
                                <label class="flex items-center gap-2 p-1.5 hover:bg-slate-50 rounded cursor-pointer text-xs">
                                    <input type="checkbox" checked value="actual" onchange="updateRadarFilter('analytic')" class="analytic-radar-cb w-3.5 h-3.5 rounded text-red-600 border-slate-300 focus:ring-red-600"> Actual
                                </label>
""" + match.group(3)
               
    content, count = re.subn(pattern, replacer, content, flags=re.DOTALL)
    
    # Also clean up the `analytic-radar-cb` from the <i> tag
    content = content.replace(
        '<i class="analytic-radar-cb fa-solid fa-chevron-down',
        '<i class="fa-solid fa-chevron-down'
    )
    # And IDP <i> tag if any
    content = content.replace(
        '<i class="idp-radar-cb fa-solid fa-chevron-down',
        '<i class="fa-solid fa-chevron-down'
    )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Patched {filepath}, count={count}")

fix_analytic_checkboxes('static/index.html')
fix_analytic_checkboxes('index_render.html')
