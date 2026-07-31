import re

with open("app.py", "r", encoding="utf-8") as f:
    content = f.read()

helper_code = """
class MockRes:
    def __init__(self, data):
        self.data = data

def fetch_all(query_builder):
    all_data = []
    start = 0
    page_size = 1000
    while True:
        res = query_builder.range(start, start + page_size - 1).execute()
        all_data.extend(res.data)
        if len(res.data) < page_size:
            break
        start += page_size
    return MockRes(all_data)

active_sessions = {}"""

if "def fetch_all(" not in content:
    content = content.replace("active_sessions = {}", helper_code)

def replace_execute(content, var_name, query_str):
    old = f'{var_name} = supabase.table{query_str}.execute()'
    new = f'{var_name} = fetch_all(supabase.table{query_str})'
    return content.replace(old, new)

content = replace_execute(content, 'comps_res', '("competencies").select("*").order("id")')
content = replace_execute(content, 'pos_res', '("positions").select("*")')
content = replace_execute(content, 'pt_res', '("position_targets").select("*").order("position_name").order("competency_idx")')
content = replace_execute(content, 'user_res', '("users").select("*")')
content = replace_execute(content, 'mgr_res', '("user_managers").select("*")')
content = replace_execute(content, 'act_res', '("user_actuals").select("*").eq("eval_year", evalYear).order("competency_idx")')
content = replace_execute(content, 'emp_res', '("all_employee_data").select("*")')

with open("app.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Fixed app.py")
