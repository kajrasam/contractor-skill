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
    return app.send_static_file('index.html')

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
            positionTargets[pos] = []
        positionTargets[pos].append(pt["target_level"])
        
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
        evidences = [a["evidence"] for a in user_acts]
        additional_expectations = [a.get("additional_expectation", "") for a in user_acts]
        learning_topics = [a.get("learning_topic", "") for a in user_acts]
        evalDate = user_acts[0]["eval_date"] if len(user_acts) > 0 and user_acts[0]["eval_date"] else ""
        
        dbUsers[uid] = {
            "pass": u["pass"],
            "role": u["role"],
            "name": u["name"],
            "position": u["position"],
            "special_expertise": u.get("special_expertise", ""),
            "special_expertise_detail": u.get("special_expertise_detail", ""),
            "actuals": actuals,
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
    evidences = data.get('evidences', [])
    additional_expectations = data.get('additionalExpectations', [])
    learning_topics = data.get('learningTopics', [])
    special_expertise = data.get('specialExpertise', "")
    special_expertise_detail = data.get('specialExpertiseDetail', "")
    evalDate = data.get('evalDate')
    
    supabase.table("users").update({
        "special_expertise": special_expertise,
        "special_expertise_detail": special_expertise_detail
    }).eq("id", uid).execute()
    
    for idx, aval in enumerate(actuals):
        evid = evidences[idx] if idx < len(evidences) else ""
        add_exp = additional_expectations[idx] if idx < len(additional_expectations) else ""
        lrn_top = learning_topics[idx] if idx < len(learning_topics) else ""
        
        supabase.table("user_actuals").update({
            "actual_level": aval,
            "evidence": evid,
            "additional_expectation": add_exp,
            "learning_topic": lrn_top,
            "eval_date": evalDate
        }).eq("user_id", uid).eq("competency_idx", idx).execute()
        
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
            "person_id": person_id,
            "employee_id": emp_id,
            "user_id": uid,
            "password": passw,
            "name_th": name,
            "name_en": f"{uid} English Name",
            "nick_name": uid[:3],
            "position_name": pos,
            "position_level": f"L{random.randint(1, 6)}",
            "section": "General",
            "department": "General",
            "sub1_division": "Sub Division 1",
            "division": "Main Division",
            "sub1_company": "Group A",
            "company": "Company A",
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

@app.route('/api/positions/targets', methods=['PUT'])
def update_position_targets():
    data = request.json
    pos = data.get('position')
    comp_idx = data.get('compIndex')
    val = data.get('value')
    
    supabase.table("position_targets").update({
        "target_level": val
    }).eq("position_name", pos).eq("competency_idx", comp_idx).execute()
    
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
    
    supabase.table("positions").update({
        "role_response": role
    }).eq("name", pos).execute()
    
    return jsonify({"status": "success"})

@app.route('/api/positions/group', methods=['PUT'])
def update_position_group():
    data = request.json
    pos = data.get('position')
    group = data.get('group')
    
    supabase.table("positions").update({
        "job_group": group
    }).eq("name", pos).execute()
    
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
        role = old_pos.data[0]['role_response']
        supabase.table("positions").insert({"name": new_name, "role_response": role}).execute()
        
        # update related
        supabase.table("position_targets").update({"position_name": new_name}).eq("position_name", old_name).execute()
        supabase.table("users").update({"position": new_name}).eq("position", old_name).execute()
        
        # delete old
        supabase.table("positions").delete().eq("name", old_name).execute()
        
    return jsonify({"status": "success"})

@app.route('/api/positions/<path:name>', methods=['DELETE'])
def delete_position(name):
    supabase.table("position_targets").delete().eq("position_name", name).execute()
    supabase.table("users").update({"position": ""}).eq("position", name).execute()
    supabase.table("positions").delete().eq("name", name).execute()
    
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(debug=True, port=3000)
