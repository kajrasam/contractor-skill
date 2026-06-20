-- Create employee_data table
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
('PER-001', 'EMP-001', 'สมชาย ใจดี', 'Somchai Jaidee', 'ชาย', 'เจ้าหน้าที่บัญชี', 'L5', 'Maintenance', 'Engineering', 'Engineering Admin', 'Commercial', 'Group A', 'Company A', 'BU1', 'Bangsue', '15511', '15511', 2039, 12, 47, 'กิตติ มั่นคง', 'PhD', 'somchai.j@example.com'),
('PER-002', 'EMP-002', 'สมศรี มีสุข', 'Somsri Meesuk', 'ศรี', 'HR BP Officer', 'L3', 'Maintenance', 'Sales', 'Sales Admin', 'Commercial', 'Group A', 'Company A', 'BU1', 'Rayong', '18271', '18271', 2031, 19, 55, 'สุรศักดิ์ พูนสวัสดิ์', 'Diploma', 'somsri.m@example.com'),
('PER-003', 'EMP-003', 'รัฐศาสตร์ มั่นคง', 'Ratthasart Mankong', 'จ้า', 'หัวหน้าหมวดซ่อม', 'L1', 'Quality Control', 'Operations', 'Operations Admin', 'Manufacturing', 'Group A', 'Company A', 'BU1', 'Chiang Mai', '57549', '57549', 2050, 11, 36, 'พรชัย รักไทย', 'Diploma', 'ratthasart.m@example.com'),
('PER-004', 'EMP-004', 'วิชัย รักไทย', 'Wichai Rakthai', 'ชัย', 'วิศวกรซ่อมบำรุง', 'L1', 'Quality Control', 'Engineering', 'Engineering Admin', 'Manufacturing', 'Group A', 'Company C', 'BU1', 'Rayong', '73566', '73566', 2054, 7, 32, 'วิชัย งามขำ', 'Diploma', 'wichai.r@example.com'),
('PER-005', 'EMP-005', 'มานะ เจริญชัย', 'Mana Charoenchai', 'นะ', 'หัวหน้างานซ่อม', 'L4', 'Quality Control', 'Engineering', 'Engineering Admin', 'Commercial', 'Group A', 'Company B', 'BU1', 'Saraburi', '95035', '95035', 2040, 6, 46, 'สมชาย วิเศษ', 'Master', 'mana.c@example.com'),
('PER-006', 'EMP-006', 'ปิติ สว่างวงศ์', 'Piti Sawangwong', 'ติ', 'ช่างซ่อมไฟฟ้า', 'L2', 'Production', 'Management', 'Management Admin', 'Commercial', 'Group A', 'Company A', 'BU1', 'Bangsue', '11462', '11462', 2061, 3, 25, 'ศิริพร บุญมาก', 'Diploma', 'piti.s@example.com'),
('PER-007', 'EMP-007', 'ชูใจ บุญมาก', 'Choojai Boonmak', 'ใจ', 'ผู้จัดการโรงงาน', 'L6', 'Payroll', 'Management', 'Management Admin', 'Commercial', 'Group A', 'Company A', 'BU1', 'Rayong', '26033', '26033', 2044, 7, 42, 'พรชัย ประเสริฐ', 'PhD', 'choojai.b@example.com'),
('PER-008', 'EMP-008', 'วีระ งามขำ', 'Weera Ngamkham', 'วี', 'ช่างซ่อมไฟฟ้า', 'L4', 'Quality Control', 'Operations', 'Operations Admin', 'Corporate', 'Group A', 'Company A', 'BU1', 'Rayong', '44044', '44044', 2056, 4, 30, 'สุรศักดิ์ วิเศษ', 'Bachelor', 'weera.n@example.com'),
('PER-009', 'EMP-009', 'อรุณ พิทักษ์', 'Arun Pitak', 'รุณ', 'ช่างซ่อมเครื่องกล', 'L3', 'Recruitment', 'Management', 'Management Admin', 'Commercial', 'Group A', 'Company B', 'BU1', 'Bangsue', '18786', '18786', 2040, 8, 46, 'สุรศักดิ์ มั่นคง', 'Diploma', 'arun.p@example.com'),
('PER-010', 'EMP-010', 'ปราณี ยอดเยี่ยม', 'Pranee Yodyeam', 'ณี', 'HR BP Officer', 'L5', 'Quality Control', 'Sales', 'Sales Admin', 'Corporate', 'Group A', 'Company C', 'BU1', 'Saraburi', '22893', '22893', 2058, 2, 28, 'กิตติ ยอดเยี่ยม', 'Diploma', 'pranee.y@example.com'),
('PER-011', 'EMP-011', 'สุรศักดิ์ สิงห์ทอง', 'Surasak Singthong', 'ศักดิ์', 'ช่างซ่อมไฟฟ้า', 'L4', 'Engineering', 'Sales', 'Sales Admin', 'Corporate', 'Group A', 'Company B', 'BU1', 'Saraburi', '29319', '29319', 2032, 31, 54, 'ชูใจ แสงทอง', 'Master', 'surasak.s@example.com'),
('PER-012', 'EMP-012', 'นภา พูนสวัสดิ์', 'Napa Poonsawat', 'ภา', 'HR BP Officer', 'L1', 'Production', 'Operations', 'Operations Admin', 'Manufacturing', 'Group A', 'Company C', 'BU1', 'Rayong', '98175', '98175', 2049, 12, 37, 'นภา ใจดี', 'Master', 'napa.p@example.com'),
('PER-013', 'EMP-013', 'กิตติ สุวรรณ', 'Kitti Suwan', 'กิต', 'ผู้จัดการโรงงาน', 'L6', 'Production', 'Finance', 'Finance Admin', 'Corporate', 'Group A', 'Company B', 'BU1', 'Saraburi', '92797', '92797', 2033, 5, 53, 'อรุณ รักไทย', 'Master', 'kitti.s@example.com'),
('PER-014', 'EMP-014', 'ศิริพร รัตน', 'Siriporn Rattana', 'พร', 'วิศวกรซ่อมบำรุง', 'L3', 'Quality Control', 'Engineering', 'Engineering Admin', 'Manufacturing', 'Group A', 'Company B', 'BU1', 'Rayong', '37972', '37972', 2061, 1, 25, 'สุมาลี รักไทย', 'High School', 'siriporn.r@example.com'),
('PER-015', 'EMP-015', 'พรชัย แสงทอง', 'Pornchai Sangthong', 'ชัย', 'หัวหน้าหมวดซ่อม', 'L6', 'Recruitment', 'Engineering', 'Engineering Admin', 'Manufacturing', 'Group A', 'Company B', 'BU1', 'Chiang Mai', '53402', '53402', 2045, 4, 41, 'ศิริพร ไพศาล', 'PhD', 'pornchai.s@example.com'),
('PER-016', 'EMP-016', 'สมบูรณ์ ทรัพย์สิริ', 'Somboon Sapsiri', 'บูลย์', 'ผู้จัดการโรงงาน', 'L4', 'Production', 'Management', 'Management Admin', 'Corporate', 'Group A', 'Company B', 'BU1', 'Rayong', '42527', '42527', 2045, 13, 41, 'วิชัย ทรัพย์สิริ', 'PhD', 'somboon.s@example.com'),
('PER-017', 'EMP-017', 'เอกราช ประเสริฐ', 'Ekarat Prasert', 'เอก', 'ช่างซ่อมไฟฟ้า', 'L6', 'Recruitment', 'Engineering', 'Engineering Admin', 'Corporate', 'Group A', 'Company B', 'BU1', 'Saraburi', '37793', '37793', 2036, 27, 50, 'วีระ ยอดเยี่ยม', 'PhD', 'ekarat.p@example.com'),
('PER-018', 'EMP-018', 'สุมาลี วิเศษ', 'Sumalee Wiset', 'มาลี', 'วิศวกรซ่อมบำรุง', 'L1', 'Production', 'Human Resources', 'Human Resources Admin', 'Commercial', 'Group A', 'Company C', 'BU1', 'Rayong', '49734', '49734', 2052, 6, 34, 'ชูใจ มีสุข', 'Master', 'sumalee.w@example.com'),
('PER-019', 'EMP-019', 'วินัย ไพศาล', 'Winai Paisal', 'นัย', 'วิศวกรซ่อมบำรุง', 'L1', 'Engineering', 'Finance', 'Finance Admin', 'Corporate', 'Group A', 'Company A', 'BU1', 'Saraburi', '45287', '45287', 2044, 8, 42, 'สมบูรณ์ ประเสริฐ', 'Master', 'winai.p@example.com'),
('PER-020', 'EMP-020', 'ธิดา เกรียงไกร', 'Thida Kriengkrai', 'ดา', 'หัวหน้าหมวดซ่อม', 'L6', 'Engineering', 'Management', 'Management Admin', 'Manufacturing', 'Group A', 'Company B', 'BU1', 'Chiang Mai', '30445', '30445', 2036, 10, 50, 'สมศรี สุวรรณ', 'High School', 'thida.k@example.com');
