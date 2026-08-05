import sys

for fp in ['index_render.html', 'static/index.html']:
    with open(fp, 'r', encoding='utf-8') as f:
        c = f.read()
    
    # Fix 1
    c = c.replace(r'\n        function openAddEmployeeModal() {', '\n        function openAddEmployeeModal() {')
    
    # Fix 2
    c = c.replace(r'populateEditEmployeeModal(emp);\n              ', 'populateEditEmployeeModal(emp);\n              ')
    
    # Fix 3
    c = c.replace(r'</div>\n              </div>\n              <div class="p-4 border-t border-slate-100 bg-slate-50 flex justify-end gap-2">', '</div>\n              </div>\n              <div class="p-4 border-t border-slate-100 bg-slate-50 flex justify-end gap-2">')

    with open(fp, 'w', encoding='utf-8') as f:
        f.write(c)
