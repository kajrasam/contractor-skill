import json
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv('d:/Work/งานใหม่/อบรม/2026/Vibe Coding Workshop/Project/competency-system/.env')
url = os.environ.get('SUPABASE_URL')
key = os.environ.get('SUPABASE_KEY')
supabase = create_client(url, key)

pos_res = supabase.table("positions").select("*").execute()
positions = [p["name"] for p in pos_res.data]

emp_res = supabase.table("employee_data").select("*").execute()
employeeData = emp_res.data

print("Positions:", positions)

# Simulate buildFiltersUI
visiblePos = positions

sectionsSet = set()
posSet = set()

for p in visiblePos:
    emps = []
    for e in employeeData:
        posName = e.get("PositionNameThai") or e.get("position_name")
        if posName:
            if posName in p or p in posName:
                emps.append(e)
    
    for e in emps:
        sec = e.get("SectionThai") or e.get("section")
        if sec: sectionsSet.add(sec)
        pname = e.get("PositionNameThai") or e.get("position_name")
        if pname: posSet.add(pname)

print("sectionsSet size:", len(sectionsSet))
print("posSet size:", len(posSet))
print("posSet:", posSet)
