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
    eval_date TEXT
);


-- Create employee_data table
DROP TABLE IF EXISTS public.employee_data;
CREATE TABLE public.employee_data (
    id SERIAL PRIMARY KEY,
    user_id TEXT UNIQUE,
    password TEXT,
    "PersonID" BIGINT,
    "PersonnelNumber" BIGINT,
    "SCGEmployeeID" BIGINT,
    "NamePrefixThai" TEXT,
    "FirstNameThai" TEXT,
    "LastNameThai" TEXT,
    "NamePrefixEnglish" TEXT,
    "FirstNameEnglish" TEXT,
    "LastNameEnglish" TEXT,
    "NickName" TEXT,
    "PositionID" BIGINT,
    "PositionNameThai" TEXT,
    "PrimaryPosition" TEXT,
    "PLGroup" TEXT,
    "OrganizationID" BIGINT,
    "Sub1ShiftThai" FLOAT,
    "ShiftThai" FLOAT,
    "Sub1SectionThai" FLOAT,
    "SectionThai" FLOAT,
    "Sub1DepartmentThai" FLOAT,
    "DepartmentThai" FLOAT,
    "Sub1DivisionThai" FLOAT,
    "DivisionThai" FLOAT,
    "Sub1CompanyThai" FLOAT,
    "CompanyThai" TEXT,
    "Sub11BusinessUnitThai" FLOAT,
    "Sub1BusinessUnitThai" FLOAT,
    "BusinessUnitDescriptionThai" TEXT,
    "PositionEnglish" TEXT,
    "Sub1ShiftEnglish" FLOAT,
    "ShiftEnglish" FLOAT,
    "Sub1SectionEnglish" FLOAT,
    "SectionEnglish" FLOAT,
    "Sub1DepartmentEnglish" FLOAT,
    "DepartmentEnglish" FLOAT,
    "Sub1DivisionEnglish" FLOAT,
    "DivisionEnglish" FLOAT,
    "Sub1CompanyEnglish" FLOAT,
    "CompanyEnglish" TEXT,
    "CompanyCode" BIGINT,
    "Sub11BusinessUnitEnglish" FLOAT,
    "Sub1BusinessUnitEnglish" FLOAT,
    "BusinessUnitDescriptionEnglish" TEXT,
    "BusinessUnitCode" TEXT,
    "OrganizationIndexForSorting" BIGINT,
    "ConsolidateCompany" TEXT,
    "HeadOfOrganizationUnit" TEXT,
    "ApproverLevelCode" FLOAT,
    "ApproverLevel" FLOAT,
    "PositionStructureLevelCode" FLOAT,
    "PositionStructureLevel" FLOAT,
    "OrgStructureLevelCode" BIGINT,
    "OrgStructureLevel" TEXT,
    "MSSSAPAuthorization" TEXT,
    "HRSAPAuthorization" TEXT,
    "PersonnelAreaCode" TEXT,
    "PersonnelArea" TEXT,
    "PersonnelSubAreaCode" TEXT,
    "PersonnelSubArea" TEXT,
    "WorkingLocationCode" TEXT,
    "WorkingLocation" TEXT,
    "EmploymentStatusText" TEXT,
    "CostCenterPayment" TEXT,
    "CostCenterOrganization" TEXT,
    "WorkContract" TEXT,
    "PayrollArea" TEXT,
    "OrgKey" TEXT,
    "ReportToPersonnelNumber" BIGINT,
    "ReportToName" TEXT,
    "ReportToPosition" BIGINT,
    "ReportToPositionName" TEXT,
    "ReportToEmail" TEXT,
    "ManagerPersonnelNumber" BIGINT,
    "ManagerName" TEXT,
    "ManagerPosition" BIGINT,
    "ManagerPositionName" TEXT,
    "ManagerEmail" TEXT,
    "TelephoneHome" BIGINT,
    "TelephoneMobile" BIGINT,
    "OfficeAddress" TEXT,
    "USER" TEXT,
    "EmailAddressBusiness" TEXT,
    "TelephoneBusiness" BIGINT,
    "TelephoneBeside" BIGINT,
    "KeyDate" TIMESTAMP WITH TIME ZONE,
    "SystemDate" TIMESTAMP WITH TIME ZONE,
    "DOALevelCode" FLOAT,
    "DOALevelText" FLOAT,
    "RecordDate" TIMESTAMP WITH TIME ZONE,
    "Pipeline" TEXT
);

INSERT INTO public.employee_data (user_id, password, "PersonID", "PersonnelNumber", "SCGEmployeeID", "NamePrefixThai", "FirstNameThai", "LastNameThai", "NamePrefixEnglish", "FirstNameEnglish", "LastNameEnglish", "NickName", "PositionID", "PositionNameThai", "PrimaryPosition", "PLGroup", "OrganizationID", "Sub1ShiftThai", "ShiftThai", "Sub1SectionThai", "SectionThai", "Sub1DepartmentThai", "DepartmentThai", "Sub1DivisionThai", "DivisionThai", "Sub1CompanyThai", "CompanyThai", "Sub11BusinessUnitThai", "Sub1BusinessUnitThai", "BusinessUnitDescriptionThai", "PositionEnglish", "Sub1ShiftEnglish", "ShiftEnglish", "Sub1SectionEnglish", "SectionEnglish", "Sub1DepartmentEnglish", "DepartmentEnglish", "Sub1DivisionEnglish", "DivisionEnglish", "Sub1CompanyEnglish", "CompanyEnglish", "CompanyCode", "Sub11BusinessUnitEnglish", "Sub1BusinessUnitEnglish", "BusinessUnitDescriptionEnglish", "BusinessUnitCode", "OrganizationIndexForSorting", "ConsolidateCompany", "HeadOfOrganizationUnit", "ApproverLevelCode", "ApproverLevel", "PositionStructureLevelCode", "PositionStructureLevel", "OrgStructureLevelCode", "OrgStructureLevel", "MSSSAPAuthorization", "HRSAPAuthorization", "PersonnelAreaCode", "PersonnelArea", "PersonnelSubAreaCode", "PersonnelSubArea", "WorkingLocationCode", "WorkingLocation", "EmploymentStatusText", "CostCenterPayment", "CostCenterOrganization", "WorkContract", "PayrollArea", "OrgKey", "ReportToPersonnelNumber", "ReportToName", "ReportToPosition", "ReportToPositionName", "ReportToEmail", "ManagerPersonnelNumber", "ManagerName", "ManagerPosition", "ManagerPositionName", "ManagerEmail", "TelephoneHome", "TelephoneMobile", "OfficeAddress", "USER", "EmailAddressBusiness", "TelephoneBusiness", "TelephoneBeside", "KeyDate", "SystemDate", "DOALevelCode", "DOALevelText", "RecordDate", "Pipeline") VALUES 
('thidas', 'Pass@1234', 324453, 2243234, 2234322, 'นาง', 'ทาทา', 'น้อยไหม', 'Mrs.', 'Tata', 'Noi', 'เอ', 90021515, 'ธุรการ', 'Y', 'M', 90000009, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'บริษัท เอสซีจี ซิเมนต์-ผลิตภัณฑ์ก่อสร้าง จำกัด', NULL, NULL, 'SCG Smart Living Business', 'Senior Secretary', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'SCG Cement-Building Materials Co.,Ltd.', 180, NULL, NULL, 'SCG Smart Living Business', 'SL', 11088, 'CONSOLIDATED', 'N', NULL, NULL, NULL, NULL, 10, 'Business Unit', 'N', 'N', 'T014', 'SCG CBM - Bangsue', 'TH04', 'Bangkok', '018T0U', 'CBM DM - Bangsue @13.805857,100.538002', 'Active', '0380-30000', '0380-30000', 'OFFICE', 'YD', 'CBM-YD-0180C-_', 90004281, 'Mr. Wiroat', 72484, 'President, SCG Smart Living Business', 'VIROJR@SCG.COM', 90004281, 'Mr. Wiroat Rattanachaisit', 72484, 'President, SCG Smart Living Business', 'VIROJR@SCG.COM', 22666677, 832456543, 'สำนักงานใหญ่ 1 ชั้น 3 ชั้น 3', 'THIDAS', 'THA@CCR.COM', 25862164, 25862164, '2026-06-19 00:00:00', '2026-06-19 00:00:00', NULL, NULL, '2026-06-18 19:15:22', 'gcrf-gcs-bigquery-orchestrator'),
('admin', 'Admin', NULL, NULL, NULL, 'คุณ', 'admin', '(Admin)', NULL, NULL, NULL, NULL, NULL, 'Admin', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'admin@company.com', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
('somchai.j', 'Pass@1234', NULL, NULL, NULL, 'คุณ', 'somchai.j', '(Admin)', NULL, NULL, NULL, NULL, NULL, 'หัวหน้างานซ่อม', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'somchai.j@company.com', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
('somsri.m', 'Pass@1234', NULL, NULL, NULL, 'คุณ', 'somsri.m', '(Admin)', NULL, NULL, NULL, NULL, NULL, 'หัวหน้าหมวดซ่อม', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'somsri.m@company.com', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
('ratthasart.m', 'Pass@1234', NULL, NULL, NULL, 'คุณ', 'ratthasart.m', '(Admin)', NULL, NULL, NULL, NULL, NULL, 'เจ้าหน้าที่บัญชี', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'ratthasart.m@company.com', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
('wichai.r', 'Pass@1234', NULL, NULL, NULL, 'คุณ', 'wichai.r', '(Admin)', NULL, NULL, NULL, NULL, NULL, 'HR BP Manager', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'wichai.r@company.com', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
('mana.c', 'Pass@1234', NULL, NULL, NULL, 'คุณ', 'mana.c', '(Admin)', NULL, NULL, NULL, NULL, NULL, 'ช่างซ่อมไฟฟ้า', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'mana.c@company.com', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
('piti.s', 'Pass@1234', NULL, NULL, NULL, 'คุณ', 'piti.s', '(Admin)', NULL, NULL, NULL, NULL, NULL, 'ผู้จัดการโรงงาน', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'piti.s@company.com', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
('choojai.b', 'Pass@1234', NULL, NULL, NULL, 'คุณ', 'choojai.b', '(Admin)', NULL, NULL, NULL, NULL, NULL, 'HR BP Officer', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'choojai.b@company.com', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
('weera.n', 'Pass@1234', NULL, NULL, NULL, 'คุณ', 'weera.n', '(Admin)', NULL, NULL, NULL, NULL, NULL, 'HR BP Officer', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'weera.n@company.com', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
('arun.p', 'Pass@1234', NULL, NULL, NULL, 'คุณ', 'arun.p', '(Admin)', NULL, NULL, NULL, NULL, NULL, 'พนักงานขาย', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'arun.p@company.com', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);
