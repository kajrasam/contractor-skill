import os
import random
from dotenv import load_dotenv
from supabase import create_client

load_dotenv('d:/Work/งานใหม่/อบรม/2026/Vibe Coding Workshop/Project/competency-system/.env')
url = os.environ.get('SUPABASE_URL')
key = os.environ.get('SUPABASE_KEY')
supabase = create_client(url, key)

# Get all users
users_res = supabase.table('users').select('*').execute()
users = users_res.data

# Get all employee_data user_ids
emp_res = supabase.table('employee_data').select('user_id').execute()
existing_uids = set([e['user_id'] for e in emp_res.data if e.get('user_id')])

inserts = []
for u in users:
    uid = u['id']
    if uid in existing_uids:
        print(f"User {uid} already in employee_data. Skipping.")
        continue
    
    # Split name to first and last if possible
    name_parts = u['name'].split(' ', 1)
    first_name = name_parts[0]
    last_name = name_parts[1] if len(name_parts) > 1 else "นามสกุล"
    
    person_id = random.randint(100000, 999999)
    personnel_num = random.randint(10000000, 99999999)
    
    # Simulate realistic organizational units based on position or id
    section = "แผนกบุคคล"
    dept = "ฝ่ายทรัพยากรบุคคล"
    sub1div = "ส่วนบริหารงานบุคคล"
    div = "ส่วนสนับสนุนธุรกิจ"
    
    lower_pos = u['position'].lower() if u.get('position') else ''
    if "me" in uid.lower() or "ee" in uid.lower() or "ช่าง" in lower_pos or "ซ่อม" in lower_pos:
        section = "แผนกซ่อมบำรุงเครื่องจักร" if "me" in uid.lower() or "เครื่องกล" in lower_pos else "แผนกซ่อมบำรุงไฟฟ้า"
        dept = "ฝ่ายซ่อมบำรุง"
        sub1div = "ส่วนปฏิบัติการซ่อมบำรุง"
        div = "ส่วนงานโรงงาน"
    
    record = {
        "user_id": uid,
        "password": u.get("pass", "password123"),
        "FullNameTH": u['name'],
        "FullNameENG": f"{first_name} English",
        "PersonID": str(person_id),
        "PersonnelNumber": str(personnel_num),
        "FirstNameThai": first_name,
        "LastNameThai": last_name,
        "FirstNameEnglish": f"{first_name}Eng",
        "LastNameEnglish": f"{last_name}Eng",
        "NickName": first_name[:3],
        "PositionNameThai": u['position'] if u.get('position') else "ไม่ระบุตำแหน่ง",
        "SectionThai": section,
        "DepartmentThai": dept,
        "Sub1DivisionThai": sub1div,
        "DivisionThai": div,
        "Sub1CompanyThai": "บริษัทในเครือ SCG",
        "CompanyThai": "SCG Group",
        "CostCenterPayment": str(random.randint(10000, 99999)),
        "CostCenterOrganization": str(random.randint(10000, 99999)),
        "EmailAddressBusiness": f"{uid.lower().replace(' ', '.')}@example.com",
        "TelephoneBusiness": f"02-555-{random.randint(1000, 9999)}",
        "ReportToName": "ผู้จัดการ ใจดี",
        "ManagerName": "ผู้อำนวยการ ใจดี",
        "WorkingLocation": "สำนักงานใหญ่",
        "EmploymentStatusText": "พนักงานประจำ",
        "WorkContract": "Full-Time"
    }
    inserts.append(record)

if inserts:
    print(f"Inserting {len(inserts)} new employees into employee_data...")
    res = supabase.table('employee_data').insert(inserts).execute()
    print("Success!")
else:
    print("No new employees to insert.")
