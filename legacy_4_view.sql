-- สร้าง SQL View สำหรับรวมข้อมูล 2 ตาราง
CREATE OR REPLACE VIEW public.all_employee_data AS
SELECT * FROM public.legacy_employee_data
UNION ALL
SELECT * FROM public.employee_data;