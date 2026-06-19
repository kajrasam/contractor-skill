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
        person_id = f"PER-GEN-{random.randint(100, 999)}"
        emp_id = f"EMP-GEN-{random.randint(100, 999)}"
        
        inserts.append({
            "person_id": person_id,
            "employee_id": emp_id,
            "user_id": uid,
            "password": u.get('pass', 'Pass@1234'),
            "name_th": u.get('name', uid),
            "name_en": f"{uid} English Name",
            "nick_name": uid[:3],
            "position_name": u.get('position', 'Staff'),
            "position_level": f"L{random.randint(1, 6)}",
            "section": random.choice(sections),
            "department": random.choice(departments),
            "sub1_division": "Sub Division 1",
            "division": "Main Division",
            "sub1_company": "Group A",
            "company": random.choice(companies),
            "sub1_1_business_unit": "BU1",
            "working_location": "Saraburi",
            "cost_center_payment": str(random.randint(10000, 99999)),
            "cost_center_organization": str(random.randint(10000, 99999)),
            "retirement_year": random.randint(2030, 2060),
            "years_of_service": random.randint(1, 20),
            "age": random.randint(25, 55),
            "report_to_name": "Manager",
            "certificate_entry_degree": "Bachelor",
            "email_address_business": f"{uid.lower()}@example.com"
        })

if inserts:
    print(f"Inserting {len(inserts)} new users into employee_data...")
    client.table("employee_data").insert(inserts).execute()
    print("Done!")
else:
    print("All users are already synced.")
