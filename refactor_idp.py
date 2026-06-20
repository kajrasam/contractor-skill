import re

files = [
    'd:/Work/งานใหม่/อบรม/2026/Vibe Coding Workshop/Project/competency-system/static/index.html',
    'd:/Work/งานใหม่/อบรม/2026/Vibe Coding Workshop/Project/competency-system/index_render.html'
]

for file_path in files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Remove variables
    content = content.replace('        let selectedIDPPos = null;\n', '')
    content = content.replace('        let selectedIDPEmp = null;\n', '')

    # 2. Remove HTML Filters block in IDP tab
    # It starts with <!-- Filters --> and ends right before <div id="idp-content-container">
    html_pattern = re.compile(
        r'<!-- Filters -->.*?<div id="idp-content-container">',
        re.DOTALL
    )
    content = html_pattern.sub('<div id="idp-content-container">', content)

    # 3. Remove buildIDPFilters call from setupIDPTab
    content = content.replace('            buildIDPFilters();\n', '')

    # 4. Replace renderIDPContent logic
    # Find start of function until `const targets = positionTargets[emp.position] || [];`
    render_start_pattern = re.compile(
        r'function renderIDPContent\(\)\s*\{.*?const emp = dbUsers\[selectedIDPEmp\];',
        re.DOTALL
    )

    new_render_start = """function renderIDPContent() {
            const container = document.getElementById('idp-content-container');
            if (!container) return;
            
            let visibleUsers = [];
            if (currentUser.id === 'Admin') {
                visibleUsers = applyGlobalFiltersToSubIds(Object.keys(dbUsers).filter(uid => uid !== 'Admin'));
            } else {
                visibleUsers = applyGlobalFiltersToSubIds([currentUser.id, ...getSubordinates(currentUser.id)]);
            }

            if (visibleUsers.length === 0) {
                container.innerHTML = `
                    <div class="bg-white p-10 rounded-2xl border border-slate-100 shadow-sm text-center text-slate-500">
                        <i class="fa-solid fa-users-slash text-4xl mb-3 text-slate-300"></i>
                        <p>ไม่พบพนักงานที่ตรงกับเงื่อนไข</p>
                    </div>`;
                return;
            }
            
            if (visibleUsers.length > 1) {
                container.innerHTML = `
                    <div class="bg-white p-10 rounded-2xl border border-slate-100 shadow-sm text-center text-slate-500">
                        <i class="fa-solid fa-address-card text-4xl mb-3 text-slate-300"></i>
                        <p>กรุณาเลือกชื่อพนักงาน 1 ท่าน จากตัวกรองด้านบนเพื่อดูแผนพัฒนา (IDP)</p>
                    </div>`;
                return;
            }

            const empId = visibleUsers[0];
            const emp = dbUsers[empId];"""
    
    content = render_start_pattern.sub(new_render_start, content)

    # 5. Remove functions buildIDPFilters, toggleIDPPosFilter, toggleIDPEmpFilter
    # They are right before renderIDPContent
    functions_pattern = re.compile(
        r'function buildIDPFilters\(\)\s*\{.*?function toggleIDPEmpFilter\(uid\)\s*\{.*?\}\n',
        re.DOTALL
    )
    content = functions_pattern.sub('', content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

print("Patch applied for IDP.")
