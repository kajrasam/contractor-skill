import random

first_names = ["สมปอง", "วิชัย", "กิตติ", "มานะ", "ปรีชา", "สมชาย", "ชาติชาย", "อารีย์", "ยุพา", "วันทนา", 
               "สมศรี", "ประยุทธ์", "สมศักดิ์", "นพดล", "ณัฐพล", "ธีรภัทร", "อนุชา", "ศักดิ์ชัย", "สุพจน์", "วสันต์",
               "วรวิทย์", "ชลธร", "ทิพวรรณ", "รัตนา", "นฤมล", "อรทัย", "จันทิมา", "วิไลพร", "ศิริพรรณ", "อุมาพร"]

last_names = ["ใจดี", "รักไทย", "คงมั่น", "สว่างวงศ์", "เจริญพร", "มีทรัพย์", "ยอดเยี่ยม", "เก่งกาจ", "มั่นคง", "บุญส่ง",
              "ทองดี", "สุขสวัสดิ์", "พิชัยญาณ", "วิเศษกุล", "รัตนพันธ์", "สิงห์ทอง", "วิริยะ", "ประเสริฐผล", "จันทร์โอชา", "ทรัพย์สิน",
              "เลิศหล้า", "มงคลชัย", "พงษ์ศักดิ์", "พิทักษ์", "ไพศาล", "รุ่งเรือง", "แสงทอง", "สุวรรณ", "เจริญชัย", "ชัยยะ"]

positions = ["ช่างซ่อมไฟฟ้า", "ช่างซ่อมเครื่องกล", "วิศวกรเครื่องกล", "วิศวกรไฟฟ้า", "พนักงานควบคุมเครื่องจักร", "หัวหน้ากะ", 
             "เจ้าหน้าที่ความปลอดภัย", "พนักงานคลังสินค้า", "พนักงานธุรการ", "วิศวกรซ่อมบำรุง"]

sections = ["หน่วยซ่อมไฟฟ้า", "หน่วยซ่อมเครื่องกล", "หน่วยผลิต 1", "หน่วยผลิต 2", "หน่วยคลังสินค้า", "หน่วยความปลอดภัย"]
departments = ["ฝ่ายซ่อมบำรุง", "ฝ่ายผลิต", "ฝ่ายซัพพลายเชน", "ฝ่ายความปลอดภัยและสิ่งแวดล้อม"]
sub1divisions = ["ส่วนงานวิศวกรรมโรงงาน", "ส่วนงานปฏิบัติการ", "ส่วนงานสนับสนุน"]
divisions = ["โรงงานสระบุรี", "โรงงานระยอง", "โรงงานบางซื่อ"]
sub1companies = ["ธุรกิจซิเมนต์", "ธุรกิจบรรจุภัณฑ์", "ธุรกิจผลิตภัณฑ์ก่อสร้าง"]
companies = ["บริษัท เอสซีจี ซิเมนต์ จำกัด", "บริษัท เอสซีจี แพคเกจจิ้ง จำกัด (มหาชน)", "บริษัท เอสซีจี รูฟฟิ่ง จำกัด"]
personnel_areas = ["Saraburi", "Rayong", "Bangkok"]
report_to_names = ["สมชาย หัวหน้างาน", "วิชัย ผู้จัดการ", "อารีย์ ไดเรกเตอร์", "กิตติ สุวรรณ", "ประยุทธ์ มั่นคง"]

users = []
for i in range(1, 31):
    first = first_names[i-1]
    last = last_names[i-1]
    eng_first = f"user{i}"
    eng_last = "test"
    
    pos = random.choice(positions)
    sec = random.choice(sections)
    dept = random.choice(departments)
    sub1div = random.choice(sub1divisions)
    div = random.choice(divisions)
    sub1comp = random.choice(sub1companies)
    comp = random.choice(companies)
    pa = random.choice(personnel_areas)
    
    manager = random.choice(report_to_names)
    mgr_email = "mgr_" + str(random.randint(1,5)) + "@company.com"
    email = f"{eng_first}@company.com"
    user_id = f"usr{i:03d}"
    
    users.append({
        "user_id": user_id,
        "password": "Password123",
        "FullName": f"{first} {last}",
        "FirstNameThai": first,
        "LastNameThai": last,
        "PositionNameThai": pos,
        "SectionThai": sec,
        "DepartmentThai": dept,
        "Sub1DivisionThai": sub1div,
        "DivisionThai": div,
        "Sub1CompanyThai": sub1comp,
        "CompanyThai": comp,
        "PersonnelArea": pa,
        "ReportToName": manager,
        "ReportToEmail": mgr_email,
        "EmailAddressBusiness": email
    })

columns = list(users[0].keys())

sql_lines = []
sql_lines.append("INSERT INTO public.employee_data (")
sql_lines.append("    " + ", ".join([f'"{c}"' for c in columns]))
sql_lines.append(") VALUES")

values_lines = []
for u in users:
    vals = []
    for c in columns:
        val = u[c]
        if val is None:
            vals.append("NULL")
        else:
            vals.append(f"'{val}'")
    values_lines.append("    (" + ", ".join(vals) + ")")

sql_lines.append(",\n".join(values_lines) + ";")

with open('insert_30_employees.sql', 'w', encoding='utf-8') as f:
    f.write("\n".join(sql_lines))

print("Created insert_30_employees.sql")
