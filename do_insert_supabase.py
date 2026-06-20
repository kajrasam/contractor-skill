import os
import sys
import importlib.util
from dotenv import load_dotenv
from supabase import create_client

# Load from specific path
spec = importlib.util.spec_from_file_location("gen_mock", "d:/Work/งานใหม่/อบรม/2026/Vibe Coding Workshop/Project/generate_mock_sql.py")
gen_mock = importlib.util.module_from_spec(spec)
sys.modules["gen_mock"] = gen_mock
spec.loader.exec_module(gen_mock)

load_dotenv('d:/Work/งานใหม่/อบรม/2026/Vibe Coding Workshop/Project/competency-system/.env')
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)

print("Clearing employee_data...")
try:
    supabase.table('employee_data').delete().neq('user_id', 'invalid_dummy_id').execute()
    print("Cleared table.")
except Exception as e:
    print(f"Error clearing: {e}")

records_to_insert = []
for r in gen_mock.records:
    rec = {}
    rec['user_id'] = r.get('user_id')
    rec['password'] = r.get('password')
    rec['FullNameTH'] = r.get('FullNameTH')
    rec['FullNameENG'] = r.get('FullNameENG')
    
    for c in gen_mock.cols:
        val = r.get(c)
        if val is not None and not isinstance(val, str) and str(val) == "nan":
            val = None
        rec[c] = val
        
    records_to_insert.append(rec)

print(f"Inserting {len(records_to_insert)} records...")
try:
    # Need to handle NaN from pandas before inserting to json
    import math
    for item in records_to_insert:
        for k, v in item.items():
            if isinstance(v, float) and math.isnan(v):
                item[k] = None
                
    res = supabase.table('employee_data').insert(records_to_insert).execute()
    print("Insertion successful!")
except Exception as e:
    print(f"Insertion failed: {e}")
