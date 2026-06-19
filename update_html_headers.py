import re

file_path = r'd:\Work\งานใหม่\อบรม\2026\Vibe Coding Workshop\Project\competency_system_dynamic_rbac_hierarchy.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

start_tag = '<th class="align-top py-4 px-6 border-r border-slate-100 bg-slate-50">Person ID</th>'
end_tag = '<th class="align-top py-4 px-6">Email Address Business</th>'

new_ths = '''<th class="align-top py-4 px-6 border-r border-slate-100 bg-slate-50 text-scg-700">USER ID</th>
                                      <th class="align-top py-4 px-6 border-r border-slate-100 text-scg-700">PASSWORD</th>
                                      <th class="align-top py-4 px-6 border-r border-slate-100">ชื่อ-นามสกุล (TH)</th>
                                      <th class="align-top py-4 px-6 border-r border-slate-100">ตำแหน่ง (POSITION)</th>
                                      <th class="align-top py-4 px-6 border-r border-slate-100">SECTION (TH)</th>
                                      <th class="align-top py-4 px-6 border-r border-slate-100">DEPARTMENT (TH)</th>
                                      <th class="align-top py-4 px-6 border-r border-slate-100">SUB1-DIVISION (TH)</th>
                                      <th class="align-top py-4 px-6 border-r border-slate-100">DIVISION (TH)</th>
                                      <th class="align-top py-4 px-6 border-r border-slate-100">SUB1-COMPANY (TH)</th>
                                      <th class="align-top py-4 px-6 border-r border-slate-100">COMPANY (TH)</th>
                                      <th class="align-top py-4 px-6 border-r border-slate-100">PERSONNEL AREA</th>
                                      <th class="align-top py-4 px-6 border-r border-slate-100">REPORT TO NAME</th>
                                      <th class="align-top py-4 px-6 border-r border-slate-100">REPORT TO EMAIL</th>
                                      <th class="align-top py-4 px-6">EMAIL ADDRESS BUSINESS</th>'''

pattern = re.compile(re.escape(start_tag) + '.*?' + re.escape(end_tag), re.DOTALL)
new_content = pattern.sub(new_ths, content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(new_content)
print('Updated HTML file headers')
