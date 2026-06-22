import json
import traceback

def patch_app_py(app_py_path):
    with open(app_py_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    if '/api/admin/sync_employees' in content:
        return "Already patched."

    new_endpoint = """
@app.route('/api/admin/sync_employees', methods=['POST'])
def sync_employees():
    data = request.json
    employees = data.get('employees', [])
    
    name_to_emp = {e.get('name_en'): e for e in employees if e.get('name_en')}
    users_to_upsert = {}
    managers_to_link = []
    
    for emp in employees:
        is_evaluated = emp.get('is_evaluated', False)
        uid = emp.get('user_id', '').strip()
        pwd = emp.get('password', '').strip()
        report_to = emp.get('report_to_name', '')
        pk_field = emp.get('pk_field')
        pk_value = emp.get('pk_value')
        name_th = emp.get('name_th', '')
        pos = emp.get('position', '')
        
        # 1. Update employee_data
        pipeline_val = "Evaluated" if is_evaluated else None
        if pk_field and pk_value:
            try:
                supabase.table("employee_data").update({
                    "user_id": uid,
                    "password": pwd,
                    "ReportToName": report_to,
                    "Pipeline": pipeline_val
                }).eq(pk_field, pk_value).execute()
            except Exception as e:
                print(f"employee_data update failed for {pk_value}: {e}")
                
        # 2. Collect for users table
        if is_evaluated and uid:
            users_to_upsert[uid] = {
                "id": uid, "pass": pwd, "role": uid, "name": name_th, "position": pos
            }
            
            # Find manager
            if report_to and report_to in name_to_emp:
                mgr = name_to_emp[report_to]
                mgr_uid = mgr.get('user_id', '').strip()
                mgr_pwd = mgr.get('password', '').strip()
                if mgr_uid:
                    managers_to_link.append({"user_id": uid, "manager_id": mgr_uid})
                    if mgr_uid not in users_to_upsert:
                        users_to_upsert[mgr_uid] = {
                            "id": mgr_uid, "pass": mgr_pwd, "role": mgr_uid, "name": mgr.get('name_th',''), "position": mgr.get('position','')
                        }

    # 3. Upsert Users
    try:
        all_comps = supabase.table("competencies").select("id").execute()
        num_comps = len(all_comps.data)
        
        for uid, udata in users_to_upsert.items():
            existing = supabase.table("users").select("id").eq("id", uid).execute()
            if existing.data:
                supabase.table("users").update(udata).eq("id", uid).execute()
            else:
                supabase.table("users").insert(udata).execute()
                # Insert defaults
                act_inserts = [{"user_id": uid, "competency_idx": i, "actual_level": 1, "evidence": "", "eval_date": ""} for i in range(num_comps)]
                if act_inserts:
                    supabase.table("user_actuals").insert(act_inserts).execute()
    except Exception as e:
        print(f"Users upsert failed: {e}")

    # 4. Sync user_managers
    try:
        # We delete all existing manager mappings for evaluated users, then insert new ones.
        for uid in users_to_upsert:
            supabase.table("user_managers").delete().eq("user_id", uid).execute()
            
        if managers_to_link:
            supabase.table("user_managers").insert(managers_to_link).execute()
    except Exception as e:
        print(f"user_managers sync failed: {e}")

    return jsonify({"status": "success", "message": "Synced successfully!"})
"""
    
    # insert before @app.route('/api/users/<uid>/manager', methods=['PUT'])
    insert_target = "@app.route('/api/users/<uid>/manager', methods=['PUT'])"
    if insert_target in content:
        content = content.replace(insert_target, new_endpoint + "\n" + insert_target)
        with open(app_py_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return "Patched app.py successfully."
    else:
        return "Target not found in app.py"

if __name__ == "__main__":
    res = patch_app_py("app.py")
    print(res)
