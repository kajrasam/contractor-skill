import random

positions = [
    "HR BP Officer", "HR BP Manager", "ช่างซ่อมไฟฟ้า", "หัวหน้างานซ่อม", "ผู้จัดการโรงงาน",
    "วิศวกรซ่อมบำรุง", "ช่างซ่อมเครื่องกล", "เจ้าหน้าที่บัญชี", "พนักงานขาย", "หัวหน้าหมวดซ่อม"
]

first_names_th = ["สมชาย", "สมศรี", "รัฐศาสตร์", "วิชัย", "มานะ", "ปิติ", "ชูใจ", "วีระ", "อรุณ", "ปราณี", "สุรศักดิ์", "นภา", "กิตติ", "ศิริพร", "พรชัย", "สมบูรณ์", "เอกราช", "สุมาลี", "วินัย", "ธิดา"]
last_names_th = ["ใจดี", "มีสุข", "มั่นคง", "รักไทย", "เจริญชัย", "สว่างวงศ์", "บุญมาก", "งามขำ", "พิทักษ์", "ยอดเยี่ยม", "สิงห์ทอง", "พูนสวัสดิ์", "สุวรรณ", "รัตน", "แสงทอง", "ทรัพย์สิริ", "ประเสริฐ", "วิเศษ", "ไพศาล", "เกรียงไกร"]
nick_names = ["ชาย", "ศรี", "จ้า", "ชัย", "นะ", "ติ", "ใจ", "วี", "รุณ", "ณี", "ศักดิ์", "ภา", "กิต", "พร", "ชัย", "บูลย์", "เอก", "มาลี", "นัย", "ดา"]
first_names_en = ["Somchai", "Somsri", "Ratthasart", "Wichai", "Mana", "Piti", "Choojai", "Weera", "Arun", "Pranee", "Surasak", "Napa", "Kitti", "Siriporn", "Pornchai", "Somboon", "Ekarat", "Sumalee", "Winai", "Thida"]
last_names_en = ["Jaidee", "Meesuk", "Mankong", "Rakthai", "Charoenchai", "Sawangwong", "Boonmak", "Ngamkham", "Pitak", "Yodyeam", "Singthong", "Poonsawat", "Suwan", "Rattana", "Sangthong", "Sapsiri", "Prasert", "Wiset", "Paisal", "Kriengkrai"]

sections = ["Recruitment", "Payroll", "Maintenance", "Production", "Accounting", "Sales", "Engineering", "Quality Control"]
departments = ["Human Resources", "Finance", "Operations", "Sales", "Engineering", "Management"]
divisions = ["Corporate", "Manufacturing", "Commercial"]
companies = ["Company A", "Company B", "Company C"]
locations = ["Bangsue", "Rayong", "Saraburi", "Chiang Mai"]
degrees = ["Bachelor", "Master", "PhD", "Diploma", "High School"]

sql = """-- Create employee_data table
DROP TABLE IF EXISTS employee_data;
CREATE TABLE employee_data (
    person_id TEXT PRIMARY KEY,
    employee_id TEXT,
    name_th TEXT,
    name_en TEXT,
    nick_name TEXT,
    position_name TEXT,
    position_level TEXT,
    section TEXT,
    department TEXT,
    sub1_division TEXT,
    division TEXT,
    sub1_company TEXT,
    company TEXT,
    sub1_1_business_unit TEXT,
    working_location TEXT,
    cost_center_payment TEXT,
    cost_center_organization TEXT,
    retirement_year INTEGER,
    years_of_service INTEGER,
    age INTEGER,
    report_to_name TEXT,
    certificate_entry_degree TEXT,
    email_address_business TEXT
);

INSERT INTO employee_data (
    person_id, employee_id, name_th, name_en, nick_name, position_name, position_level,
    section, department, sub1_division, division, sub1_company, company, sub1_1_business_unit,
    working_location, cost_center_payment, cost_center_organization, retirement_year, years_of_service,
    age, report_to_name, certificate_entry_degree, email_address_business
) VALUES
"""

values = []
for i in range(20):
    person_id = f"PER-{i+1:03d}"
    employee_id = f"EMP-{i+1:03d}"
    idx = i % len(first_names_th)
    name_th = f"{first_names_th[idx]} {last_names_th[idx]}"
    name_en = f"{first_names_en[idx]} {last_names_en[idx]}"
    nick_name = nick_names[idx]
    pos = random.choice(positions)
    level = random.choice(["L1", "L2", "L3", "L4", "L5", "L6"])
    sec = random.choice(sections)
    dept = random.choice(departments)
    sub1_div = f"{dept} Admin"
    div = random.choice(divisions)
    sub1_comp = "Group A"
    comp = random.choice(companies)
    bu = "BU1"
    loc = random.choice(locations)
    cc_pay = f"{random.randint(10000, 99999)}"
    cc_org = cc_pay
    age = random.randint(25, 55)
    yos = random.randint(1, age - 22)
    ret_year = 2026 + (60 - age)
    manager = random.choice(first_names_th) + " " + random.choice(last_names_th)
    deg = random.choice(degrees)
    email = f"{first_names_en[idx].lower()}.{last_names_en[idx][0].lower()}@example.com"

    val = f"('{person_id}', '{employee_id}', '{name_th}', '{name_en}', '{nick_name}', '{pos}', '{level}', '{sec}', '{dept}', '{sub1_div}', '{div}', '{sub1_comp}', '{comp}', '{bu}', '{loc}', '{cc_pay}', '{cc_org}', {ret_year}, {yos}, {age}, '{manager}', '{deg}', '{email}')"
    values.append(val)

sql += ",\n".join(values) + ";\n"

with open("employee_data.sql", "w", encoding="utf-8") as f:
    f.write(sql)
