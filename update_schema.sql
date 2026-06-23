-- Drop existing table
DROP TABLE IF EXISTS public.employee_data;

-- Create simplified employee_data table
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
    "JobGroup" TEXT
);

-- Insert basic Admin and Mock users
INSERT INTO public.employee_data (
    user_id, password, "PersonnelNumber", "FullName", "PositionNameThai", "PositionStructureLevel", "SectionThai", "DepartmentThai", "Sub1DivisionThai", "DivisionThai", "Sub1CompanyThai", "CompanyThai", "ReportToName", "Certificate", "JobGroup"
) VALUES 
('admin', 'Admin', NULL, 'System Admin (HR)', 'Admin', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'Admin'),
('somchai.j', 'Pass@1234', '1001', 'สมชาย มีทรัพย์ (Admin)', 'หัวหน้างานซ่อม', 'PL2', 'หน่วยซ่อมเครื่องกล', 'ฝ่ายซ่อมบำรุง', 'ส่วนงานวิศวกรรมโรงงาน', 'โรงงานบางซื่อ', 'ธุรกิจซิเมนต์', 'บริษัท เอสซีจี แพคเกจจิ้ง จำกัด (มหาชน)', 'ประยุทธ์ มั่นคง', 'ปริญญาตรี', 'ช่างเทคนิค'),
('somsri.m', 'Pass@1234', '1002', 'สมศรี ทองดี (Admin)', 'หัวหน้าหมวดซ่อม', 'PL3', 'หน่วยซ่อมไฟฟ้า', 'ฝ่ายซ่อมบำรุง', 'ส่วนงานวิศวกรรมโรงงาน', 'โรงงานสระบุรี', 'ธุรกิจบรรจุภัณฑ์', 'บริษัท เอสซีจี แพคเกจจิ้ง จำกัด (มหาชน)', 'สมชาย มีทรัพย์', 'ปริญญาตรี', 'ช่างเทคนิค');
