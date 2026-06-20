import os
import random
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
client = create_client(url, key)

print("Fetching existing users and employee data...")
res_users = client.table("users").select("*").execute()
users = res_users.data

res_emp = client.table("employee_data").select("user_id").execute()
existing_user_ids = [e['user_id'] for e in res_emp.data if e.get('user_id')]

departments = ['Production', 'Engineering', 'Finance', 'Human Resources', 'Sales', 'Maintenance']
sections = ['Operations Admin', 'Engineering Admin', 'Finance Admin', 'HR Admin', 'Sales Admin', 'Maintenance Admin']
companies = ['Company A', 'Company B', 'Company C']

inserts = []
for u in users:
    uid = u['id']
    if uid not in existing_user_ids:
        # Generate mock data
        inserts.append({
            "user_id": uid,
            "password": u.get('pass', 'Pass@1234'),
            "FullName": u.get('name', uid),
            "FirstNameThai": uid,
            "LastNameThai": "Mock",
            "PositionNameThai": u.get('position', 'Staff'),
            "SectionThai": random.choice(sections),
            "DepartmentThai": random.choice(departments),
            "Sub1DivisionThai": "Sub Division 1",
            "DivisionThai": "Main Division",
            "Sub1CompanyThai": "Group A",
            "CompanyThai": random.choice(companies),
            "PersonnelArea": "Saraburi",
            "ReportToName": "Manager",
            "ReportToEmail": f"mgr_{uid}@example.com",
            "EmailAddressBusiness": f"{uid.lower()}@example.com"
        })

if inserts:
    print(f"Inserting {len(inserts)} new users into employee_data...")
    client.table("employee_data").insert(inserts).execute()
    print("Done!")
else:
    print("All users are already synced.")
