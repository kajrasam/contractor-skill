import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def seed_db():
    print("Checking if db is empty...")
    users = supabase.table("users").select("id").limit(1).execute()
    if len(users.data) > 0:
        print("Database already contains data. Skipping seed.")
        return

    print("Seeding competencies...")
    comps = [
        {"original_id": "c1", "name": "1. งานซ่อมไฟฟ้า (EE)", "icon": "fa-bolt", "type": "Functional", "l1": "รู้จักอุปกรณ์เบื้องต้น (เรียกชื่อเบรกเกอร์ได้)", "l2": "ทำ PM พื้นฐานตามคู่มือได้", "l3": "ปฏิบัติงานและเปลี่ยนอะไหล่ได้อิสระ", "l4": "วิเคราะห์วงจรซับซ้อน/สอนผู้อื่นได้", "l5": "วางแผน/ออกแบบปรับปรุงประสิทธิภาพระบบไฟฟ้า"},
        {"original_id": "c2", "name": "2. งานซ่อมเครื่องกล (ME)", "icon": "fa-gear", "type": "Functional", "l1": "รู้จักชิ้นส่วนเครื่องกลพื้นฐาน", "l2": "ทำการหล่อลื่นและเปลี่ยนชิ้นส่วนง่ายๆได้", "l3": "ซ่อมบำรุงและตั้งศูนย์เครื่องจักรได้ (Alignment)", "l4": "วิเคราะห์หาสาเหตุการสั่นสะเทือน/ความร้อนได้", "l5": "ออกแบบปรับปรุงกลไกเพื่อเพิ่มอายุการใช้งาน (MTBF)"},
        {"original_id": "c3", "name": "3. การวิเคราะห์/แก้ปัญหา", "icon": "fa-magnifying-glass-chart", "type": "Functional", "l1": "แจ้งอาการเสียได้ถูกต้อง", "l2": "แก้ไขอาการเสียประจำหน้างานได้", "l3": "ใช้เครื่องมือวัดหาสาเหตุเชิงลึกได้", "l4": "แก้ปัญหาระบบเชื่อมโยงข้ามเครื่องจักร", "l5": "วิเคราะห์ Root Cause และวางมาตรการป้องกันถาวร"},
        {"original_id": "c4", "name": "4. ความปลอดภัย/LOTO", "icon": "fa-shield-halved", "type": "Functional", "l1": "สวม PPE และทราบกฎเบื้องต้น", "l2": "เตรียมอุปกรณ์ LOTO ถูกต้อง", "l3": "ปฏิบัติ LOTO เดี่ยวได้สมบูรณ์", "l4": "เป็นผู้นำควบคุม Group LOTO", "l5": "ตรวจสอบและประเมินความเสี่ยง JSA/ร่างมาตรฐาน"},
        {"original_id": "c5", "name": "5. การทำงานเป็นทีม", "icon": "fa-people-group", "type": "Core", "l1": "รับฟังและปฏิบัติตามคำสั่ง", "l2": "สื่อสารส่งมอบงานในกะได้ชัดเจน", "l3": "ร่วมมือประสานงานกับแผนกอื่น", "l4": "ไกล่เกลี่ยและลดความขัดแย้งหน้างาน", "l5": "สร้างบรรยากาศและเป็นผู้นำทีมข้ามสายงาน"},
        {"original_id": "c6", "name": "6. การเรียนรู้อย่างต่อเนื่อง", "icon": "fa-book-open", "type": "Core", "l1": "เข้ารับการอบรมตามกำหนด", "l2": "สอบถามเมื่อเจอสิ่งใหม่", "l3": "ศึกษาคู่มือ Manual ด้วยตนเอง", "l4": "นำความรู้ใหม่มาประยุกต์ใช้จริง", "l5": "ริเริ่มและผลักดันนวัตกรรมในแผนก"},
        {"original_id": "c7", "name": "7. การสอนงาน", "icon": "fa-chalkboard-user", "type": "Leadership", "l1": "แนะนำสถานที่และกฎระเบียบเบื้องต้น", "l2": "ให้คำแนะนำเทคนิคสั้นๆ", "l3": "สอนงานหน้างาน (OJT) เป็นขั้นตอนได้", "l4": "จัดทำเอกสารคู่มือ One Point Lesson (OPL)", "l5": "เป็นวิทยากรภายใน (Internal Trainer)"}
    ]
    supabase.table("competencies").insert(comps).execute()

    print("Seeding positions...")
    pos_data = [
        {"name": "หัวหน้างานซ่อม (Supervisor)", "role_response": "ดูแลและควบคุมงานซ่อมบำรุงทั้งระบบไฟฟ้าและเครื่องกล บริหารจัดการทรัพยากรและบุคคล"},
        {"name": "หัวหน้าหมวดซ่อม (Teamleader)", "role_response": "รับผิดชอบงานซ่อมบำรุงเฉพาะหมวด (ไฟฟ้า/เครื่องกล) ตามที่ได้รับมอบหมาย ควบคุมงานของช่าง"},
        {"name": "ช่างชำนาญงานซ่อมไฟฟ้า (SpecialistEE)", "role_response": "แก้ไขปัญหาและบำรุงรักษาระบบไฟฟ้าที่ซับซ้อน เป็นพี่เลี้ยงให้ช่างซ่อมไฟฟ้า"},
        {"name": "ช่างชำนาญงานซ่อมเครื่องกล (SpecialistME)", "role_response": "แก้ไขปัญหาและบำรุงรักษาเครื่องจักรกลที่ซับซ้อน เป็นพี่เลี้ยงให้ช่างซ่อมเครื่องกล"},
        {"name": "ช่างซ่อม ไฟฟ้า (EmployeeEE)", "role_response": "ปฏิบัติงานซ่อมบำรุงระบบไฟฟ้าตามแผน PM และแก้ไขปัญหาหน้างานเบื้องต้น"},
        {"name": "ช่างซ่อม เครื่องกล (EmployeeME)", "role_response": "ปฏิบัติงานซ่อมบำรุงเครื่องจักรกลตามแผน PM และเปลี่ยนชิ้นส่วนตามคู่มือ"}
    ]
    supabase.table("positions").insert(pos_data).execute()

    print("Seeding position_targets...")
    targets = {
        "หัวหน้างานซ่อม (Supervisor)":         [4, 4, 5, 5, 5, 5, 5],
        "หัวหน้าหมวดซ่อม (Teamleader)":        [4, 4, 4, 5, 4, 4, 4],
        "ช่างชำนาญงานซ่อมไฟฟ้า (SpecialistEE)": [5, 2, 4, 5, 4, 4, 4],
        "ช่างชำนาญงานซ่อมเครื่องกล (SpecialistME)":[2, 5, 4, 5, 4, 4, 4],
        "ช่างซ่อม ไฟฟ้า (EmployeeEE)":         [3, 0, 2, 4, 3, 3, 0],
        "ช่างซ่อม เครื่องกล (EmployeeME)":     [0, 3, 2, 4, 3, 3, 0]
    }
    pt_inserts = []
    for pos, tlist in targets.items():
        for idx, tval in enumerate(tlist):
            pt_inserts.append({"position_name": pos, "competency_idx": idx, "target_level": tval})
    supabase.table("position_targets").insert(pt_inserts).execute()

    print("Seeding users...")
    users = [
        {"id": "Admin", "pass": "0817906628", "role": "Admin", "name": "System Admin (HR)", "position": "Admin"},
        {"id": "Supervisor", "pass": "Supervisor", "role": "Supervisor", "name": "นาย สมศักดิ์ (Supervisor)", "position": "หัวหน้างานซ่อม (Supervisor)"},
        {"id": "Teamleader", "pass": "Teamleader", "role": "Teamleader", "name": "นาย สมชาย (Teamleader)", "position": "หัวหน้าหมวดซ่อม (Teamleader)"},
        {"id": "SpecialistEE", "pass": "SpecialistEE", "role": "SpecialistEE", "name": "นาย ไฟฟ้า (SpecialistEE)", "position": "ช่างชำนาญงานซ่อมไฟฟ้า (SpecialistEE)"},
        {"id": "SpecialistME", "pass": "SpecialistME", "role": "SpecialistME", "name": "นาย เครื่องกล (SpecialistME)", "position": "ช่างชำนาญงานซ่อมเครื่องกล (SpecialistME)"},
        {"id": "EmployeeEE", "pass": "EmployeeEE", "role": "EmployeeEE", "name": "นาย สายไฟ (EmployeeEE)", "position": "ช่างซ่อม ไฟฟ้า (EmployeeEE)"},
        {"id": "EmployeeME", "pass": "EmployeeME", "role": "EmployeeME", "name": "นาย เฟือง (EmployeeME)", "position": "ช่างซ่อม เครื่องกล (EmployeeME)"}
    ]
    supabase.table("users").insert(users).execute()

    print("Seeding user_managers...")
    managers = [
        {"user_id": "Teamleader", "manager_id": "Supervisor"},
        {"user_id": "SpecialistEE", "manager_id": "Teamleader"},
        {"user_id": "SpecialistME", "manager_id": "Teamleader"},
        {"user_id": "EmployeeEE", "manager_id": "SpecialistEE"},
        {"user_id": "EmployeeME", "manager_id": "SpecialistME"}
    ]
    supabase.table("user_managers").insert(managers).execute()

    print("Seeding user_actuals...")
    user_actuals_data = {
        "Admin": [0,0,0,0,0,0,0],
        "Supervisor": [4,3,4,5,5,4,4],
        "Teamleader": [3,4,4,5,4,4,3],
        "SpecialistEE": [5,1,3,5,4,3,3],
        "SpecialistME": [1,4,3,4,3,4,3],
        "EmployeeEE": [2,0,2,3,2,2,0],
        "EmployeeME": [0,2,2,3,3,2,0]
    }
    ua_inserts = []
    for uid, alist in user_actuals_data.items():
        for idx, aval in enumerate(alist):
            ua_inserts.append({"user_id": uid, "competency_idx": idx, "actual_level": aval, "evidence": "", "eval_date": ""})
    # Supabase REST limits insert size, but we have 49 rows so it's fine.
    supabase.table("user_actuals").insert(ua_inserts).execute()
    
    print("Seed complete!")

if __name__ == '__main__':
    seed_db()
