-- Drop existing tables if they exist (Be careful if you have existing data!)
DROP TABLE IF EXISTS user_actuals;
DROP TABLE IF EXISTS position_targets;
DROP TABLE IF EXISTS positions;
DROP TABLE IF EXISTS competencies;
DROP TABLE IF EXISTS user_managers;
DROP TABLE IF EXISTS users;

-- Create users table
CREATE TABLE users (
    id TEXT PRIMARY KEY,
    pass TEXT,
    role TEXT,
    name TEXT,
    position TEXT,
    special_expertise TEXT,
    special_expertise_detail TEXT
);

-- Create user_managers table
CREATE TABLE user_managers (
    user_id TEXT,
    manager_id TEXT
);

-- Create competencies table
CREATE TABLE competencies (
    id SERIAL PRIMARY KEY,
    original_id TEXT,
    name TEXT,
    icon TEXT,
    type TEXT,
    l1 TEXT,
    l2 TEXT,
    l3 TEXT,
    l4 TEXT,
    l5 TEXT,
    competency_group TEXT
);

-- Create positions table
CREATE TABLE positions (
    name TEXT PRIMARY KEY,
    role_response TEXT,
    job_group TEXT
);

-- Create position_targets table
CREATE TABLE position_targets (
    position_name TEXT,
    competency_idx INTEGER,
    target_level INTEGER
);

-- Create user_actuals table
CREATE TABLE user_actuals (
    user_id TEXT,
    competency_idx INTEGER,
    actual_level INTEGER,
    evidence TEXT,
    additional_expectation TEXT,
    learning_topic TEXT,
    eval_date TEXT,
    eval_status TEXT,
    eval_year INTEGER
);


-- Create employee_data table
DROP TABLE IF EXISTS public.employee_data;
CREATE TABLE public.employee_data (
    id SERIAL PRIMARY KEY,
    user_id TEXT UNIQUE,
    password TEXT,
    "PersonnelNumber" TEXT,
    "FullName" TEXT,
    "PositionNameThai" TEXT,
    "PositionStructureLevel" TEXT,
    "SectionThai" TEXT,
    "DepartmentThai" TEXT,
    "Sub1DivisionThai" TEXT,
    "DivisionThai" TEXT,
    "Sub1CompanyThai" TEXT,
    "CompanyThai" TEXT,
    "ReportToName" TEXT,
    "Certificate" TEXT,
    "JobGroup" TEXT,
    "Email" TEXT
);

INSERT INTO public.employee_data (
    user_id, password, "PersonnelNumber", "FullName", "PositionNameThai", "PositionStructureLevel", "SectionThai", "DepartmentThai", "Sub1DivisionThai", "DivisionThai", "Sub1CompanyThai", "CompanyThai", "ReportToName", "Certificate", "JobGroup", "Email"
) VALUES 
('admin', 'Admin', NULL, 'System Admin (HR)', 'Admin', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'Admin', NULL),
('somchai.j', 'Pass@1234', '1001', 'สมชาย มีทรัพย์ (Admin)', 'หัวหน้างานซ่อม', 'PL2', 'หน่วยซ่อมเครื่องกล', 'ฝ่ายซ่อมบำรุง', 'ส่วนงานวิศวกรรมโรงงาน', 'โรงงานบางซื่อ', 'ธุรกิจซิเมนต์', 'บริษัท เอสซีจี แพคเกจจิ้ง จำกัด (มหาชน)', 'ประยุทธ์ มั่นคง', 'ปริญญาตรี', 'ช่างเทคนิค', 'somchai.j@example.com'),
('somsri.m', 'Pass@1234', '1002', 'สมศรี ทองดี (Admin)', 'หัวหน้าหมวดซ่อม', 'PL3', 'หน่วยซ่อมไฟฟ้า', 'ฝ่ายซ่อมบำรุง', 'ส่วนงานวิศวกรรมโรงงาน', 'โรงงานสระบุรี', 'ธุรกิจบรรจุภัณฑ์', 'บริษัท เอสซีจี แพคเกจจิ้ง จำกัด (มหาชน)', 'สมชาย มีทรัพย์', 'ปริญญาตรี', 'ช่างเทคนิค', 'somsri.m@example.com');
