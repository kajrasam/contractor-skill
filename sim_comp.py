import os
import json
from dotenv import load_dotenv
from supabase import create_client

load_dotenv('d:/Work/งานใหม่/อบรม/2026/Vibe Coding Workshop/Project/competency-system/.env')
url = os.environ.get('SUPABASE_URL')
key = os.environ.get('SUPABASE_KEY')
supabase = create_client(url, key)

pt_res = supabase.table('position_targets').select('*').order('position_name').order('competency_idx').execute()
positionTargets = {}
for pt in pt_res.data:
    pos = pt['position_name']
    if pos not in positionTargets:
        positionTargets[pos] = []
    positionTargets[pos].append(pt['target_level'])

comps_res = supabase.table('competencies').select('*').order('id').execute()
competencies = []
for comp in comps_res.data:
    competencies.append({
        "name": comp["name"],
        "group": comp.get("competency_group", "")
    })

visiblePos = [
    'Admin', 'HR', 'ช่างชำนาญงานซ่อมเครื่องกล (SpecialistME)', 'ช่างชำนาญงานซ่อมไฟฟ้า (SpecialistEE)', 
    'ช่างซ่อม', 'ช่างซ่อม เครื่องกล (EmployeeME)', 'ช่างซ่อม ไฟฟ้า (EmployeeEE)', 
    'พนักงานธุรการ', 'วิศวกร', 'หัวหน้างาน', 'หัวหน้างานซ่อม (Supervisor)', 'หัวหน้าหมวดซ่อม'
]

visibleCompSet = set()
for p in visiblePos:
    if p in positionTargets:
        for i, t in enumerate(positionTargets[p]):
            if t > 0:
                visibleCompSet.add(i)

visibleComps = sorted(list(visibleCompSet))
print("visibleComps length:", len(visibleComps))

rows_rendered = 0
for i in visibleComps:
    if i >= len(competencies):
        print(f"Index {i} OUT OF BOUNDS for competencies (len {len(competencies)})")
        continue
    comp = competencies[i]
    if not comp:
        print(f"Comp {i} is falsy!")
        continue
    rows_rendered += 1

print("Rows rendered:", rows_rendered)
