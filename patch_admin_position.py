import re

def patch_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Update the header
    old_header = """<th class="py-3 px-4 border-r border-slate-100">Name (TH)</th>
                                    <th class="py-3 px-4 border-r border-slate-100">Name (EN)</th>"""
    new_header = """<th class="py-3 px-4 border-r border-slate-100">Name (TH)</th>
                                    <th class="py-3 px-4 border-r border-slate-100">Position Name</th>
                                    <th class="py-3 px-4 border-r border-slate-100">Name (EN)</th>"""
    
    # ensure it only replaces the first occurrence (in the admin table)
    # The second occurrence in the Employee Data table has different classes
    html = html.replace(old_header, new_header)

    # 2. Update the row rendering
    old_row = """<td class="py-2 px-4 border-r border-slate-100">${emp.name_th}</td>
                        <td class="py-2 px-4 border-r border-slate-100">${emp.name_en}</td>"""
    new_row = """<td class="py-2 px-4 border-r border-slate-100">${emp.name_th}</td>
                        <td class="py-2 px-4 border-r border-slate-100 text-xs text-slate-500">${eData ? (eData.PositionNameThai || eData.position_name || '-') : '-'}</td>
                        <td class="py-2 px-4 border-r border-slate-100">${emp.name_en}</td>"""
    
    html = html.replace(old_row, new_row)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Patched {filepath}")

patch_file('static/index.html')
patch_file('index_render.html')
