
import sys
import re

md_content = """# คู่มือการใช้งานสำหรับผู้ดูแลระบบ (Admin & Super Admin Manual)

คู่มือฉบับนี้จัดทำขึ้นเพื่อเป็นแนวทางสำหรับ **ผู้ดูแลระบบ (Admin)** และ **ผู้ดูแลระบบสูงสุด (Super Admin/HR)** ในการบริหารจัดการระบบ Contractor-skill อย่างมีประสิทธิภาพ

---

## 1. ทำความเข้าใจระดับสิทธิ์ (Roles & Permissions)

ในระบบจะแบ่งระดับสิทธิ์ของผู้ดูแลระบบออกเป็น 2 ระดับหลัก ได้แก่:

1. **Super Admin (System Admin - HR):**
   - มีสิทธิ์สูงสุดในระบบ สามารถมองเห็นข้อมูลของพนักงานทั้งหมดในบริษัท
   - สามารถจัดการผู้ดูแลระบบ (Admin) ท่านอื่นๆ ได้
   - มีสิทธิ์ในการตั้งค่าระดับความคาดหวัง (Target Competency) ของทุกตำแหน่ง
2. **Admin (ผู้ดูแลระดับหน่วยงาน):**
   - สามารถจัดการข้อมูลพนักงาน กำหนดสิทธิ์ และดูรายงานได้ **เฉพาะภายในขอบเขต (Scope)** ที่ตนเองได้รับมอบหมายเท่านั้น (เช่น ดูแลเฉพาะ Division หรือ Department ของตนเอง)

---

## 2. ภาพรวมขั้นตอนการทำงานของ Admin (Workflow)

แผนภาพด้านล่างแสดงลำดับขั้นตอนการทำงานหลักที่ Admin ต้องดูแลในระบบ:

<div class="mermaid-wrapper my-6 bg-slate-50 p-6 rounded-xl border border-slate-100 flex justify-center">
<pre class="mermaid">
graph TD
    A[Admin เข้าสู่ระบบ] --> B{ต้องการทำอะไร?}
    B -->|พนักงานเข้าใหม่| C[เมนู Admin: สร้าง User ใหม่]
    C --> D[กำหนดตำแหน่ง & สิทธิ์การใช้งาน]
    D --> E[กำหนดขอบเขต (Scope) หากเป็น Admin/Supervisor]
    
    B -->|ติดตามความคืบหน้า| F[เมนู ติดตามการประเมิน]
    F --> G[ตรวจสอบว่าพนักงานประเมินตนเองหรือยัง?]
    F --> H[ตรวจสอบว่าหัวหน้าประเมิน Before/After หรือยัง?]
    G & H --> I[Export Excel เพื่อสรุปผลรายงาน]
    
    B -->|วิเคราะห์ภาพรวม| J[เมนู Dashboard / Analytic]
    J --> K[ดูความพร้อมของทีม / Top Performers]
    J --> L[วางแผนพัฒนา (IDP) ให้ทีม]
</pre>
</div>

---

## 3. การจัดการผู้ใช้งาน (User Management)

เมนูหลักสำหรับการจัดการพนักงานคือเมนู **"⚙️ Admin"** (มุมซ้ายล่างของหน้าจอ)

### 3.1 การเพิ่มผู้ใช้งานใหม่ (Add User)
1. ไปที่เมนู **Admin** 
2. คลิกปุ่ม **"+ Add New User"** (เพิ่มผู้ใช้ใหม่)
3. กรอกข้อมูลส่วนตัวของพนักงาน:
   - **รหัสพนักงาน (Employee ID / Username):** ใช้สำหรับ Login
   - **รหัสผ่าน (Password):** ตั้งรหัสผ่านเริ่มต้น
   - **ชื่อ-นามสกุล, ตำแหน่ง, ฝ่าย (Department), ฯลฯ**
4. เลือกระดับสิทธิ์ (Role):
   - `USER`: พนักงานทั่วไป ประเมินตนเองได้อย่างเดียว
   - `SUPERVISOR`: หัวหน้างาน สามารถประเมินลูกน้องได้
   - `ADMIN` / `SUPER_ADMIN`: ผู้ดูแลระบบ
5. **(สำคัญ)** หากตั้งให้เป็น `ADMIN` หรือ `SUPERVISOR` ระบบจะให้คุณระบุ **Scope (ขอบเขตการดูแล)** เช่น ให้ดูแลเฉพาะ Division: "Concrete Technology" เป็นต้น
6. กดปุ่ม **"Save"** เพื่อบันทึกข้อมูล

### 3.2 การแก้ไข / ลบ ผู้ใช้งาน
- **การแก้ไข:** ค้นหาชื่อพนักงานในตารางหน้า Admin แล้วคลิกปุ่ม **"Edit" (ไอคอนดินสอ)** เพื่อแก้ไขข้อมูล ตำแหน่ง หรือปรับเปลี่ยน Scope
- **การลบ:** คลิกปุ่ม **"Delete" (ไอคอนถังขยะ)** ท้ายชื่อพนักงาน (ระบบจะถามเพื่อยืนยันก่อนลบเสมอ)

<div class="bg-red-50 border-l-4 border-red-500 p-4 my-4 rounded-r-lg">
  <div class="flex items-center">
    <i class="fa-solid fa-triangle-exclamation text-red-500 mr-2"></i>
    <strong class="text-red-700">ข้อควรระวัง (Warning)</strong>
  </div>
  <p class="text-red-600 mt-2 text-sm">การลบผู้ใช้งานจะทำให้ข้อมูลการประเมินของพนักงานคนนั้นหายไปจากระบบ หากพนักงานลาออก แนะนำให้ใช้วิธี <b>ระงับการใช้งาน (Inactive)</b> หากระบบมีรองรับ หรือเปลี่ยนรหัสผ่านเพื่อไม่ให้เข้าสู่ระบบได้แทน</p>
</div>

---

## 4. การติดตามการประเมิน (Evaluation Tracking)

Admin มีหน้าที่สำคัญในการติดตามว่าพนักงานและหัวหน้างานดำเนินการประเมินครบถ้วนหรือไม่ โดยไปที่เมนู **"ติดตามการประเมิน"**

**สิ่งที่ Admin ต้องตรวจสอบ:**
1. **คอลัมน์ "ประเมินตนเอง":** หากมีวันที่แสดง แปลว่าพนักงานประเมินตนเองแล้ว
2. **คอลัมน์ "ประเมิน(Before)":** หากมีวันที่แสดง แปลว่าหัวหน้าได้ประเมินระดับทักษะก่อนการพัฒนาแล้ว
3. **คอลัมน์ "ประเมิน(After)":** หากมีวันที่แสดง แปลว่าหัวหน้าได้ประเมินระดับทักษะปัจจุบัน (Actual) แล้ว

<div class="bg-blue-50 border-l-4 border-blue-500 p-4 my-4 rounded-r-lg">
  <div class="flex items-center">
    <i class="fa-solid fa-lightbulb text-blue-500 mr-2"></i>
    <strong class="text-blue-700">คำแนะนำ (Tip)</strong>
  </div>
  <p class="text-blue-600 mt-2 text-sm">Admin สามารถกดปุ่ม <b>"Export Excel"</b> มุมขวาบน เพื่อดาวน์โหลดตารางติดตามการประเมินออกไปสรุปเป็นรายงานรายสัปดาห์/รายเดือน เพื่อติดตามทวงถามพนักงานที่ยังไม่ประเมินได้ทันที</p>
</div>

---

## 5. การวิเคราะห์ข้อมูลสำหรับ Admin (Data Analytics)

เมื่อการประเมินเสร็จสิ้น Admin สามารถใช้ข้อมูลเพื่อวางแผนพัฒนาบุคลากรได้:

- **Dashboard:** ดูภาพรวม Gap ของทักษะในหน่วยงาน และ Average Skill Level ของทีม เปรียบเทียบระหว่าง เป้าหมาย (Expected), ก่อนพัฒนา (Before), ประเมินตนเอง (Self), และปัจจุบัน (Actual)
- **Competency Analytic:** วิเคราะห์พนักงานที่เป็น **Top Performers** (ผู้มีความพร้อมสูงสุด) และค้นหาทักษะที่เป็นจุดแข็งหรือจุดที่หน่วยงานต้องเร่งจัดอบรม
- **IDP (Individual Development Plan):** เข้าไปดูแผนพัฒนารายบุคคลของพนักงานแต่ละคน เพื่อดูคอร์สเรียนแนะนำ (Training Need)

---

<div class="bg-amber-50 border-l-4 border-amber-500 p-4 my-4 rounded-r-lg">
  <div class="flex items-center">
    <i class="fa-solid fa-circle-info text-amber-500 mr-2"></i>
    <strong class="text-amber-700">หมายเหตุ (Note)</strong>
  </div>
  <p class="text-amber-600 mt-2 text-sm">คู่มือนี้เป็นคู่มือสรุปขั้นตอนการทำงานหลัก หากมีข้อสงสัยหรือพบ Error ในการใช้งาน สามารถติดต่อทีมงานผู้พัฒนาระบบเพื่อแก้ไขได้ตลอดเวลา</p>
</div>
"""

try:
    import markdown
    html_body = markdown.markdown(md_content)
except ImportError:
    # Basic replacement if markdown library is missing
    html_body = md_content.replace('\n\n', '</p><p>').replace('\n', '<br>')

# Manually fix up some headers for basic styling if markdown failed
html_body = re.sub(r'^# (.*?)$', r'<h1 class="text-3xl font-black text-scg-800 mb-6 border-b pb-4">\1</h1>', html_body, flags=re.MULTILINE)
html_body = re.sub(r'^## (.*?)$', r'<h2 class="text-2xl font-bold text-scg-700 mt-10 mb-4">\1</h2>', html_body, flags=re.MULTILINE)
html_body = re.sub(r'^### (.*?)$', r'<h3 class="text-xl font-bold text-slate-700 mt-6 mb-3">\1</h3>', html_body, flags=re.MULTILINE)

html_template = f"""<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>คู่มือการใช้งานระบบสำหรับผู้ดูแลระบบ (Admin Manual)</title>
    
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Prompt:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
    
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {{
            theme: {{
                extend: {{
                    fontFamily: {{
                        sans: ['Prompt', 'sans-serif'],
                    }},
                    colors: {{
                        scg: {{
                            50: '#fdf2f2',
                            100: '#fbe5e5',
                            200: '#f6cdce',
                            300: '#f0aab0',
                            400: '#e57782',
                            500: '#d7485a',
                            600: '#c13048',
                            700: '#a22339',
                            800: '#872033',
                            900: '#711f2f',
                        }}
                    }}
                }}
            }}
        }}
    </script>

    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <style>
        body {{
            background-color: #f8fafc;
            color: #334155;
        }}
        .manual-container {{
            max-width: 900px;
            margin: 40px auto;
            background: white;
            padding: 50px 60px;
            border-radius: 20px;
            box-shadow: 0 10px 40px -10px rgba(0,0,0,0.08);
        }}
        
        @media print {{
            body {{
                background-color: white;
            }}
            .manual-container {{
                margin: 0;
                padding: 0;
                box-shadow: none;
                max-width: 100%;
            }}
            .no-print {{
                display: none !important;
            }}
        }}

        h1, h2, h3 {{
            color: #a22339; /* scg-700 */
        }}
        
        hr {{
            border-color: #e2e8f0;
            margin: 2rem 0;
        }}

        ul, ol {{
            padding-left: 1.5rem;
            margin-bottom: 1rem;
        }}
        
        ul {{
            list-style-type: disc;
        }}
        
        ol {{
            list-style-type: decimal;
        }}
        
        li {{
            margin-bottom: 0.5rem;
            line-height: 1.6;
        }}
        
        code {{
            background-color: #f1f5f9;
            padding: 0.2rem 0.4rem;
            border-radius: 0.25rem;
            font-size: 0.875em;
            color: #e11d48;
        }}
    </style>
</head>
<body class="antialiased">

    <!-- Print Button Bar (Hidden in print) -->
    <div class="no-print fixed top-0 left-0 right-0 bg-white shadow-sm border-b border-slate-200 py-3 px-6 z-50 flex justify-between items-center">
        <div class="flex items-center text-scg-700 font-bold">
            <i class="fa-solid fa-book-open mr-2 text-xl"></i>
            Contractor-skill Admin Manual
        </div>
        <div>
            <button onclick="window.print()" class="bg-scg-600 hover:bg-scg-700 text-white px-5 py-2 rounded-lg font-medium shadow-sm transition-colors flex items-center gap-2">
                <i class="fa-solid fa-print"></i> 
                Print / Save as PDF
            </button>
        </div>
    </div>

    <!-- Main Content -->
    <div class="pt-16 pb-12 px-4">
        <div class="manual-container relative">
            {html_body}
        </div>
    </div>

    <!-- Mermaid JS -->
    <script type="module">
        import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
        mermaid.initialize({{ 
            startOnLoad: true,
            theme: 'base',
            themeVariables: {{
                primaryColor: '#fbe5e5',
                primaryTextColor: '#872033',
                primaryBorderColor: '#e57782',
                lineColor: '#cbd5e1',
                secondaryColor: '#f1f5f9',
                tertiaryColor: '#fff'
            }}
        }});
    </script>
</body>
</html>
"""

with open('admin_manual.html', 'w', encoding='utf-8') as f:
    f.write(html_template)

print("Generated admin_manual.html")
