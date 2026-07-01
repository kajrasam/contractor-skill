import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

app = Flask(__name__, static_folder='static', static_url_path='')
CORS(app)

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

@app.route('/')
def index():
    response = app.send_static_file('index.html')
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/api/data', methods=['GET'])
def get_data():
    # 1. competencies
    comps_res = supabase.table("competencies").select("*").order("id").execute()
    competencies = []
    for comp in comps_res.data:
        competencies.append({
            "id": comp["original_id"],
            "name": comp["name"],
            "icon": comp["icon"],
            "type": comp["type"],
            "group": comp.get("competency_group", ""),
            "levels": {
                1: comp["l1"],
                2: comp["l2"],
                3: comp["l3"],
                4: comp["l4"],
                5: comp["l5"]
            }
        })
        
    # 2. positions and roleResponses
    pos_res = supabase.table("positions").select("*").execute()
    positions = []
    roleResponses = {}
    positionGroups = {}
    for p in pos_res.data:
        positions.append(p["name"])
        roleResponses[p["name"]] = p["role_response"]
        positionGroups[p["name"]] = p.get("job_group", "")
        
    # 3. positionTargets
    pt_res = supabase.table("position_targets").select("*").order("position_name").order("competency_idx").execute()
    positionTargets = {}
    for pt in pt_res.data:
        pos = pt["position_name"]
        if pos not in positionTargets:
            positionTargets[pos] = [0] * len(competencies)
        idx = pt["competency_idx"]
        if idx < len(competencies):
            positionTargets[pos][idx] = pt["target_level"]
        
    # 4. dbUsers
    user_res = supabase.table("users").select("*").execute()
    mgr_res = supabase.table("user_managers").select("*").execute()
    act_res = supabase.table("user_actuals").select("*").order("competency_idx").execute()
    
    dbUsers = {}
    for u in user_res.data:
        uid = u["id"]
        
        # get managers
        mgrs = [m["manager_id"] for m in mgr_res.data if m["user_id"] == uid]
        
        # get actuals
        user_acts = [a for a in act_res.data if a["user_id"] == uid]
        actuals = [a["actual_level"] for a in user_acts]
        self_evals = [a.get("self_level") for a in user_acts]
        before_evals = [a.get("before_level") for a in user_acts]
        supervisor_feedback = [a.get("supervisor_feedback", "") for a in user_acts]
        evidences = [a["evidence"] for a in user_acts]
        additional_expectations = [a.get("additional_expectation", "") for a in user_acts]
        learning_topics = [a.get("learning_topic", "") for a in user_acts]
        evalDate = user_acts[0]["eval_date"] if len(user_acts) > 0 and user_acts[0]["eval_date"] else ""
        
        scope_sec = ""
        scope_dep = ""
        scope_div = []
        detail = u.get("special_expertise_detail", "")
        if u["role"] == "Admin" and detail and detail.startswith("{"):
            import json
            try:
                parsed = json.loads(detail)
                scope_sec = parsed.get("scope_section", "")
                scope_dep = parsed.get("scope_department", "")
                scope_div = parsed.get("scope_division", [])
            except:
                pass

        dbUsers[uid] = {
            "scope_section": scope_sec,
            "scope_department": scope_dep,
            "scope_division": scope_div,
            "pass": u["pass"],
            "role": u["role"],
            "name": u["name"],
            "position": u["position"],
            "special_expertise": u.get("special_expertise", ""),
            "special_expertise_detail": detail,
            "actuals": actuals,
            "self_evals": self_evals,
            "before_evals": before_evals,
            "supervisor_feedback": supervisor_feedback,
            "evidences": evidences,
            "additional_expectations": additional_expectations,
            "learning_topics": learning_topics,
            "managerIds": mgrs,
            "evalDate": evalDate
        }
        
    # 5. employee_data
    employeeData = []
    try:
        emp_res = supabase.table("employee_data").select("*").execute()
        employeeData = emp_res.data
    except Exception as e:
        print(f"Warning: could not fetch employee_data: {e}")

    return jsonify({
        "competencies": competencies,
        "positions": positions,
        "positionTargets": positionTargets,
        "roleResponses": roleResponses,
        "positionGroups": positionGroups,
        "dbUsers": dbUsers,
        "employeeData": employeeData
    })

@app.route('/api/evaluations', methods=['PUT'])
def update_evaluation():
    data = request.json
    uid = data.get('userId')
    actuals = data.get('actuals', [])
    self_evals = data.get('selfEvals', [])
    before_evals = data.get('beforeEvals', [])
    supervisor_feedbacks = data.get('supervisorFeedbacks', [])
    evidences = data.get('evidences', [])
    additional_expectations = data.get('additionalExpectations', [])
    learning_topics = data.get('learningTopics', [])
    special_expertise = data.get('specialExpertise', "")
    special_expertise_detail = data.get('specialExpertiseDetail', "")
    evalDate = data.get('evalDate')
    evalStatus = data.get('evalStatus', "")
    
    try:
        supabase.table("users").update({
            "special_expertise": special_expertise,
            "special_expertise_detail": special_expertise_detail
        }).eq("id", uid).execute()
    except Exception as e:
        print(f"Failed to update users {uid}: {e}")
    
    for idx, aval in enumerate(actuals):
        sval = self_evals[idx] if idx < len(self_evals) else None
        bval = before_evals[idx] if idx < len(before_evals) else None
        sfb = supervisor_feedbacks[idx] if idx < len(supervisor_feedbacks) else ""
        evid = evidences[idx] if idx < len(evidences) else ""
        add_exp = additional_expectations[idx] if idx < len(additional_expectations) else ""
        lrn_top = learning_topics[idx] if idx < len(learning_topics) else ""
        
        try:
            existing = supabase.table("user_actuals").select("user_id").eq("user_id", uid).eq("competency_idx", idx).execute()
            if existing.data:
                supabase.table("user_actuals").update({
                    "actual_level": aval,
                    "self_level": sval,
                    "before_level": bval,
                    "supervisor_feedback": sfb,
                    "evidence": evid,
                    "additional_expectation": add_exp,
                    "learning_topic": lrn_top,
                    "eval_date": evalDate,
                    "eval_status": evalStatus
                }).eq("user_id", uid).eq("competency_idx", idx).execute()
            else:
                supabase.table("user_actuals").insert({
                    "user_id": uid,
                    "competency_idx": idx,
                    "actual_level": aval,
                    "self_level": sval,
                    "before_level": bval,
                    "supervisor_feedback": sfb,
                    "evidence": evid,
                    "additional_expectation": add_exp,
                    "learning_topic": lrn_top,
                    "eval_date": evalDate,
                    "eval_status": evalStatus
                }).execute()
        except Exception as e:
            print(f"Failed to update user_actuals {uid} {idx}: {e}")
        
    return jsonify({"status": "success"})

@app.route('/api/admin_users', methods=['POST'])
def add_admin_user():
    data = request.json
    uid = data.get('uid')
    passw = data.get('pass')
    name = data.get('name')
    scope_sec = data.get('scope_section', '')
    scope_dep = data.get('scope_department', '')
    scope_div = data.get('scope_division', [])
    
    existing = supabase.table("users").select("id").eq("id", uid).execute()
    import json
    detail = json.dumps({"scope_section": scope_sec, "scope_department": scope_dep, "scope_division": scope_div})
    
    if len(existing.data) > 0:
        supabase.table("users").update({"pass": passw, "name": name, "special_expertise_detail": detail}).eq("id", uid).execute()
    else:
        supabase.table("users").insert({"id": uid, "pass": passw, "role": "Admin", "name": name, "position": "Admin", "special_expertise_detail": detail}).execute()
    return jsonify({"status": "success"})

@app.route('/api/admin_users/<uid>', methods=['DELETE'])
def delete_admin_user(uid):
    supabase.table("users").delete().eq("id", uid).execute()
    return jsonify({"status": "success"})

@app.route('/api/users', methods=['POST'])
def add_user():
    data = request.json
    uid = data.get('uid')
    passw = data.get('pass')
    name = data.get('name')
    pos = data.get('pos')
    mgrs = data.get('mgrs')
    num_comps = data.get('num_comps', 7)
    
    # Check if user exists
    existing = supabase.table("users").select("id").eq("id", uid).execute()
    if len(existing.data) > 0:
        return jsonify({"status": "error", "message": "Username exists"}), 400
        
    supabase.table("users").insert({
        "id": uid, "pass": passw, "role": uid, "name": name, "position": pos
    }).execute()
    
    # Auto-generate employee data profile
    import random
    person_id = f"PER-GEN-{random.randint(100, 999)}"
    emp_id = f"EMP-GEN-{random.randint(100, 999)}"
    
    try:
        supabase.table("employee_data").insert({
            "PersonnelNumber": str(random.randint(1000000, 9999999)),
            "user_id": uid,
            "password": passw,
            "FullName": name,
            "PositionNameThai": pos,
            "PositionStructureLevel": "",
            "SectionThai": "General",
            "DepartmentThai": "General",
            "Sub1DivisionThai": "Sub Division 1",
            "DivisionThai": "Main Division",
            "Sub1CompanyThai": "Group A",
            "CompanyThai": "Company A",
            "ReportToName": "Manager",
            "Certificate": "",
            "JobGroup": ""
        }).execute()
    except Exception as e:
        print("Failed to auto-generate employee_data:", e)

    if mgrs:
        mgr_inserts = [{"user_id": uid, "manager_id": m} for m in mgrs]
        supabase.table("user_managers").insert(mgr_inserts).execute()
        
    act_inserts = [{"user_id": uid, "competency_idx": i, "actual_level": 1, "evidence": "", "eval_date": ""} for i in range(num_comps)]
    if act_inserts:
        supabase.table("user_actuals").insert(act_inserts).execute()
        
    return jsonify({"status": "success"})


@app.route('/api/admin/sync_employees', methods=['POST'])
def sync_employees():
    data = request.json
    employees = data.get('employees', [])
    deleted_ids = data.get('deleted_ids', [])
    
    # Process deletions first
    if deleted_ids:
        try:
            # Get the user_ids associated with these employee_data rows to delete them from users table
            del_emps = supabase.table("employee_data").select("id, user_id").in_("id", deleted_ids).execute()
            del_uids = [e['user_id'] for e in del_emps.data if e.get('user_id')]
            
            # Delete from employee_data
            supabase.table("employee_data").delete().in_("id", deleted_ids).execute()
            
            # Delete related data from users and other tables
            if del_uids:
                supabase.table("user_actuals").delete().in_("user_id", del_uids).execute()
                supabase.table("user_managers").delete().in_("user_id", del_uids).execute()
                supabase.table("user_managers").delete().in_("manager_id", del_uids).execute()
                supabase.table("users").delete().in_("id", del_uids).execute()
        except Exception as e:
            print(f"Delete failed: {e}")

    name_to_emp = {e.get('name_th'): e for e in employees if e.get('name_th')}
    name_en_to_emp = {e.get('name_en'): e for e in employees if e.get('name_en')}
    # Merge mappings for fallback
    name_to_emp.update(name_en_to_emp)
    
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
        is_new = emp.get('is_new', False)
        
        # 1. Update or Insert employee_data
        if is_new:
            try:
                new_data = {
                    "user_id": uid,
                    "password": pwd,
                    "PersonnelNumber": emp.get('person_id', ''),
                    "FullName": name_th,
                    "PositionNameThai": pos,
                    "PositionStructureLevel": emp.get('position_level', ''),
                    "SectionThai": emp.get('section', ''),
                    "DepartmentThai": emp.get('department', ''),
                    "Sub1DivisionThai": emp.get('sub1_division', ''),
                    "DivisionThai": emp.get('division', ''),
                    "Sub1CompanyThai": emp.get('sub1_company', ''),
                    "CompanyThai": emp.get('company', ''),
                    "ReportToName": report_to,
                    "Certificate": emp.get('certificate', ''),
                    "JobGroup": emp.get('job_group', ''),
                    "Email": emp.get('email', ''),
                    "Pipeline": "Evaluated" if is_evaluated else None
                }
                supabase.table("employee_data").insert(new_data).execute()
            except Exception as e:
                print(f"employee_data insert failed for {name_th}: {e}")
        elif pk_field and pk_value:
            try:
                supabase.table("employee_data").update({
                    "user_id": uid,
                    "password": pwd,
                    "PersonnelNumber": emp.get('person_id', ''),
                    "FullName": name_th,
                    "PositionNameThai": pos,
                    "PositionStructureLevel": emp.get('position_level', ''),
                    "SectionThai": emp.get('section', ''),
                    "DepartmentThai": emp.get('department', ''),
                    "Sub1DivisionThai": emp.get('sub1_division', ''),
                    "DivisionThai": emp.get('division', ''),
                    "Sub1CompanyThai": emp.get('sub1_company', ''),
                    "CompanyThai": emp.get('company', ''),
                    "ReportToName": report_to,
                    "Certificate": emp.get('certificate', ''),
                    "JobGroup": emp.get('job_group', ''),
                    "Email": emp.get('email', ''),
                    "Pipeline": "Evaluated" if is_evaluated else None
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

@app.route('/api/users/<uid>/manager', methods=['PUT'])
def update_user_manager(uid):
    data = request.json
    mgrs = data.get('managers', [])
    
    supabase.table("user_managers").delete().eq("user_id", uid).execute()
    if mgrs:
        mgr_inserts = [{"user_id": uid, "manager_id": m} for m in mgrs]
        supabase.table("user_managers").insert(mgr_inserts).execute()
        
    return jsonify({"status": "success"})

@app.route('/api/competencies', methods=['POST'])
def add_competency():
    data = request.json
    name = data.get('name')
    icon = data.get('icon', 'fa-star')
    cid = data.get('id')
    
    res = supabase.table("competencies").insert({
        "original_id": cid, "name": name, "icon": icon, "type": "Functional",
        "l1": "", "l2": "", "l3": "", "l4": "", "l5": ""
    }).execute()
    
    all_comps = supabase.table("competencies").select("id").execute()
    comp_idx = len(all_comps.data) - 1
    
    # Update position targets
    pos_res = supabase.table("positions").select("name").execute()
    pt_inserts = [{"position_name": p["name"], "competency_idx": comp_idx, "target_level": 0} for p in pos_res.data]
    if pt_inserts:
        supabase.table("position_targets").insert(pt_inserts).execute()
        
    # Update user actuals
    user_res = supabase.table("users").select("id").execute()
    ua_inserts = [{"user_id": u["id"], "competency_idx": comp_idx, "actual_level": 1, "evidence": "", "eval_date": ""} for u in user_res.data]
    if ua_inserts:
        supabase.table("user_actuals").insert(ua_inserts).execute()
        
    return jsonify({"status": "success"})

@app.route('/api/competencies/levels', methods=['PUT'])
def update_competency_levels():
    data = request.json
    idx = data.get('index')
    levels = data.get('levels') # dict with 1,2,3,4,5
    
    # Since we need to update by ID, we need the actual id of the competency at `idx`
    comps = supabase.table("competencies").select("id").order("id").execute()
    if idx < len(comps.data):
        real_id = comps.data[idx]['id']
        supabase.table("competencies").update({
            "l1": levels.get('1',''),
            "l2": levels.get('2',''),
            "l3": levels.get('3',''),
            "l4": levels.get('4',''),
            "l5": levels.get('5','')
        }).eq("id", real_id).execute()
        
    return jsonify({"status": "success"})

@app.route('/api/positions/target', methods=['PUT'])
def update_position_target():
    data = request.json
    pos = data.get('position')
    comp_idx = data.get('compIndex')
    val = data.get('value')
    
    try:
        existing = supabase.table("position_targets").select("position_name").eq("position_name", pos).eq("competency_idx", comp_idx).execute()
        if existing.data:
            supabase.table("position_targets").update({
                "target_level": val
            }).eq("position_name", pos).eq("competency_idx", comp_idx).execute()
        else:
            supabase.table("position_targets").insert({
                "position_name": pos,
                "competency_idx": comp_idx,
                "target_level": val
            }).execute()
    except Exception as e:
        print(f"Failed to update position_targets for {pos} idx {comp_idx}: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500
    
    return jsonify({"status": "success"})

@app.route('/api/positions', methods=['POST'])
def add_position():
    data = request.json
    pos = data.get('name')
    num_comps = data.get('num_comps', 7)
    
    supabase.table("positions").insert({
        "name": pos, "role_response": "ระบุหน้าที่ความรับผิดชอบ..."
    }).execute()
    
    pt_inserts = [{"position_name": pos, "competency_idx": i, "target_level": 0} for i in range(num_comps)]
    if pt_inserts:
        supabase.table("position_targets").insert(pt_inserts).execute()
        
    return jsonify({"status": "success"})

@app.route('/api/positions/role', methods=['PUT'])
def update_position_role():
    data = request.json
    pos = data.get('position')
    role = data.get('roleResponse')
    
    try:
        existing = supabase.table("positions").select("name").eq("name", pos).execute()
        if existing.data:
            supabase.table("positions").update({
                "role_response": role
            }).eq("name", pos).execute()
        else:
            supabase.table("positions").insert({
                "name": pos,
                "role_response": role
            }).execute()
    except Exception as e:
        print(f"Failed to update role_response for {pos}: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500
        
    return jsonify({"status": "success"})

@app.route('/api/positions/group', methods=['PUT'])
def update_position_group():
    data = request.json
    pos = data.get('position')
    group = data.get('group')
    
    try:
        existing = supabase.table("positions").select("name").eq("name", pos).execute()
        if existing.data:
            supabase.table("positions").update({
                "job_group": group
            }).eq("name", pos).execute()
        else:
            supabase.table("positions").insert({
                "name": pos,
                "job_group": group
            }).execute()
    except Exception as e:
        print(f"Failed to update job_group for {pos}: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500
        
    return jsonify({"status": "success"})

@app.route('/api/competencies/group', methods=['PUT'])
def update_competency_group():
    data = request.json
    idx = data.get('index')
    group = data.get('group')
    
    comps = supabase.table("competencies").select("id").order("id").execute()
    if idx < len(comps.data):
        real_id = comps.data[idx]['id']
        supabase.table("competencies").update({
            "competency_group": group
        }).eq("id", real_id).execute()
        
    return jsonify({"status": "success"})

@app.route('/api/competencies/name', methods=['PUT'])
def update_competency_name():
    data = request.json
    idx = data.get('index')
    name = data.get('name')
    
    comps = supabase.table("competencies").select("id").order("id").execute()
    if idx < len(comps.data):
        real_id = comps.data[idx]['id']
        supabase.table("competencies").update({
            "name": name
        }).eq("id", real_id).execute()
        
    return jsonify({"status": "success"})

@app.route('/api/positions/name', methods=['PUT'])
def update_position_name():
    data = request.json
    old_name = data.get('oldName')
    new_name = data.get('newName')
    
    # We must insert the new position first because name is Primary Key
    old_pos = supabase.table("positions").select("*").eq("name", old_name).execute()
    if old_pos.data:
        role = old_pos.data[0].get('role_response', '')
        jg = old_pos.data[0].get('job_group', '')
        supabase.table("positions").insert({"name": new_name, "role_response": role, "job_group": jg}).execute()
        
        # update related
        supabase.table("position_targets").update({"position_name": new_name}).eq("position_name", old_name).execute()
        supabase.table("users").update({"position": new_name}).eq("position", old_name).execute()
        supabase.table("employee_data").update({"PositionNameThai": new_name}).eq("PositionNameThai", old_name).execute()
        
        # delete old
        supabase.table("positions").delete().eq("name", old_name).execute()
        
    return jsonify({"status": "success"})

@app.route('/api/positions/<path:name>', methods=['DELETE'])
def delete_position(name):
    supabase.table("position_targets").delete().eq("position_name", name).execute()
    supabase.table("users").update({"position": ""}).eq("position", name).execute()
    supabase.table("positions").delete().eq("name", name).execute()
    
    return jsonify({"status": "success"})

@app.route('/api/competencies/<int:idx>', methods=['DELETE'])
def delete_competency(idx):
    comps = supabase.table("competencies").select("id").order("id").execute()
    if idx < len(comps.data):
        real_id = comps.data[idx]['id']
        supabase.table("position_targets").delete().eq("competency_idx", idx).execute()
        supabase.table("user_actuals").delete().eq("competency_idx", idx).execute()
        supabase.table("competencies").delete().eq("id", real_id).execute()
        
        # We need to shift competency_idx for position_targets and user_actuals
        # because the frontend uses array index. This is a complex operation.
        # Given the frontend logic, deleting a competency splices the array, 
        # meaning all subsequent indices decrease by 1.
        targets = supabase.table("position_targets").select("*").gte("competency_idx", idx + 1).execute()
        for t in targets.data:
            supabase.table("position_targets").update({"competency_idx": t["competency_idx"] - 1}).eq("position_name", t["position_name"]).eq("competency_idx", t["competency_idx"]).execute()
            
        actuals = supabase.table("user_actuals").select("*").gte("competency_idx", idx + 1).execute()
        for a in actuals.data:
            supabase.table("user_actuals").update({"competency_idx": a["competency_idx"] - 1}).eq("user_id", a["user_id"]).eq("competency_idx", a["competency_idx"]).execute()
        
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(debug=True, port=3000)
