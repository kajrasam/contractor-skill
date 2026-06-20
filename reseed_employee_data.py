import os
import random
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY'))

# Fetch all users
res = supabase.table('employee_data').select('*').execute()
users = res.data

companies = ['บริษัท เอสซีจี รูฟฟิ่ง เซรามิคพาร์ท จำกัด', 'บริษัท ปูนซิเมนต์ไทย (ท่าหลวง) จำกัด', 'บริษัท ผลิตภัณฑ์คอนกรีตซีแพค จำกัด', 'SCG Chemicals', 'SCG Packaging']
departments = ['Accounting', 'Engineering', 'Human Resources', 'Sales', 'Production', 'Quality Control', 'Maintenance']
sections = ['Finance', 'Recruitment', 'Operations', 'Management', 'R&D']
locations = ['CBM DM - Bangsue', 'Saraburi Plant', 'Rayong Plant', 'Chiang Mai Office']
pl_groups = ['L1', 'L2', 'L3', 'L4', 'L5', 'M', 'S']

print(f"Found {len(users)} users to update.")

for u in users:
    update_data = {}
    
    # Generate missing PersonID and SCGEmployeeID
    if not u.get('PersonID'):
        update_data['PersonID'] = str(random.randint(100000, 999999))
    if not u.get('SCGEmployeeID'):
        update_data['SCGEmployeeID'] = str(random.randint(2000000, 2999999))
        
    # Generate English Name if missing
    if not u.get('FirstNameEnglish'):
        first_th = u.get('FirstNameThai', '')
        # Simple romanization mock
        update_data['NamePrefixEnglish'] = random.choice(['Mr.', 'Mrs.', 'Ms.'])
        update_data['FirstNameEnglish'] = first_th.capitalize() if first_th else f"User{u['id']}"
        update_data['LastNameEnglish'] = "Scg"
        
    if not u.get('NickName'):
        update_data['NickName'] = f"Nick{u['id']}"
        
    if not u.get('PLGroup'):
        update_data['PLGroup'] = random.choice(pl_groups)
        
    if not u.get('CompanyThai'):
        update_data['CompanyThai'] = random.choice(companies)
    if not u.get('Sub1CompanyThai'):
        update_data['Sub1CompanyThai'] = "SCG Group"
    if not u.get('DivisionThai'):
        update_data['DivisionThai'] = "Corporate"
    if not u.get('Sub1DivisionThai'):
        update_data['Sub1DivisionThai'] = "Corporate Admin"
    if not u.get('DepartmentThai'):
        update_data['DepartmentThai'] = random.choice(departments)
    if not u.get('SectionThai'):
        update_data['SectionThai'] = random.choice(sections)
        
    if not u.get('WorkingLocation'):
        update_data['WorkingLocation'] = random.choice(locations)
        
    if not u.get('CostCenterPayment'):
        update_data['CostCenterPayment'] = f"0{random.randint(100, 999)}-30000"
    if not u.get('CostCenterOrganization'):
        update_data['CostCenterOrganization'] = update_data.get('CostCenterPayment', u.get('CostCenterPayment'))
        
    if not u.get('ManagerName'):
        update_data['ManagerName'] = "Mr. Wiroat Rattanachaisit"
        
    if not u.get('EmailAddressBusiness'):
        uid = u.get('id')
        update_data['EmailAddressBusiness'] = f"{u.get('user_id') or f'user{uid}'}@scg.com"
        
    # Extra fields (removed age and years_of_service as they don't exist in schema)
    # Just update the rest
    
    if update_data:
        try:
            supabase.table('employee_data').update(update_data).eq('id', u['id']).execute()
            print(f"Updated user ID {u['id']} ({u.get('user_id')}) with {len(update_data)} fields.")
        except Exception as e:
            print(f"Failed to update user ID {u['id']}: {e}")

print("Successfully seeded all missing data in Supabase.")
