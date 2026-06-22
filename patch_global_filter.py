import re

def patch_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Fix buildFiltersUI
    # Find buildFiltersUI and replace employeeData.forEach with employeeDataAll.forEach inside it
    idx = html.find('function buildFiltersUI()')
    end = html.find('}', html.find('let allCompanies', idx) if html.find('let allCompanies', idx) != -1 else html.find('employee-dropdown-text', idx))
    if end == -1:
        end = idx + 5000 # fallback
        
    build_code = html[idx:end]
    build_code = build_code.replace('employeeData.forEach(e => {', 'employeeDataAll.forEach(e => {')
    html = html[:idx] + build_code + html[end:]

    # 2. Remove "ถูกประเมิน" column
    # The header
    html = html.replace(
        '<th class="align-top py-4 px-6 border-r border-slate-100 text-center text-scg-600">ถูกประเมิน</th>\n                                    <th class="align-top py-4 px-6 border-r border-slate-100 text-scg-700">User ID</th>',
        '<th class="align-top py-4 px-6 border-r border-slate-100 text-scg-700">User ID</th>'
    )
    # The row
    html = html.replace(
        '<td class="py-3 px-6 border-r border-slate-100 text-center"><i class="fa-solid fa-check-circle text-green-500 text-lg" title="Evaluated"></i></td>\n                        <td class="py-3 px-6 border-r border-slate-100 text-scg-700 font-medium">${emp.user_id || emp.username || emp.USER || \'-\'}</td>',
        '<td class="py-3 px-6 border-r border-slate-100 text-scg-700 font-medium">${emp.user_id || emp.username || emp.USER || \'-\'}</td>'
    )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Patched {filepath}")

patch_file('static/index.html')
patch_file('index_render.html')
