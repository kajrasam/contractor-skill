import re

def inject_manual_tab(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update Navigation Menu (renderNav)
    nav_old = r'''(html \+= `<button onclick="switchTab\('admin'\)" id="nav-admin"[^>]+>.*?</button>`;)'''
    nav_new = r'''\1
                html += `<button onclick="switchTab('admin-manual')" id="nav-admin-manual" class="nav-btn w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-all text-left text-scg-700 bg-scg-50 hover:bg-scg-100 mt-1"><i class="fa-solid fa-book-open w-5 text-center"></i> คู่มือ Admin</button>`;'''
    content = re.sub(nav_old, nav_new, content)

    # 2. Update switchTab function to include admin-manual in tabsWithFilters
    # Actually admin-manual doesn't need filters, so it shouldn't be in tabsWithFilters
    # But we need to make sure the tab can be activated. switchTab uses `tab-${tabId}`.

    # 3. Add Tab Content Section
    manual_content = """
<!-- Admin Manual Tab -->
<section id="tab-admin-manual" class="tab-content hidden">
    <div class="bg-white rounded-2xl shadow-sm border border-slate-100 p-8 max-w-5xl mx-auto my-6">
        <div class="flex justify-between items-center mb-8 pb-4 border-b">
            <h1 class="text-3xl font-black text-scg-800">คู่มือการใช้งานสำหรับผู้ดูแลระบบ (Admin Manual)</h1>
            <a href="admin_manual.html" target="_blank" class="bg-scg-600 hover:bg-scg-700 text-white px-5 py-2 rounded-lg font-medium shadow-sm transition-colors flex items-center gap-2">
                <i class="fa-solid fa-arrow-up-right-from-square"></i> เปิดหน้าต่างใหม่ / Print
            </a>
        </div>

        <p class="mb-6 text-slate-600">คู่มือฉบับนี้จัดทำขึ้นเพื่อเป็นแนวทางสำหรับ <strong>ผู้ดูแลระบบ (Admin)</strong> และ <strong>ผู้ดูแลระบบสูงสุด (Super Admin/HR)</strong> ในการบริหารจัดการระบบ Contractor-skill อย่างมีประสิทธิภาพ</p>

        <h2 class="text-2xl font-bold text-scg-700 mt-10 mb-4">1. ทำความเข้าใจระดับสิทธิ์ (Roles & Permissions)</h2>
        <p class="mb-4 text-slate-600">ในระบบจะแบ่งระดับสิทธิ์ของผู้ดูแลระบบออกเป็น 2 ระดับหลัก ได้แก่:</p>
        <ol class="list-decimal pl-6 space-y-2 mb-6 text-slate-600">
            <li><strong>Super Admin (System Admin - HR):</strong>
                <ul class="list-disc pl-6 mt-1 space-y-1">
                    <li>มีสิทธิ์สูงสุดในระบบ สามารถมองเห็นข้อมูลของพนักงานทั้งหมดในบริษัท</li>
                    <li>สามารถจัดการผู้ดูแลระบบ (Admin) ท่านอื่นๆ ได้</li>
                    <li>มีสิทธิ์ในการตั้งค่าระดับความคาดหวัง (Target Competency) ของทุกตำแหน่ง</li>
                </ul>
            </li>
            <li><strong>Admin (ผู้ดูแลระดับหน่วยงาน):</strong>
                <ul class="list-disc pl-6 mt-1 space-y-1">
                    <li>สามารถจัดการข้อมูลพนักงาน กำหนดสิทธิ์ และดูรายงานได้ <strong>เฉพาะภายในขอบเขต (Scope)</strong> ที่ตนเองได้รับมอบหมายเท่านั้น (เช่น ดูแลเฉพาะ Division หรือ Department ของตนเอง)</li>
                </ul>
            </li>
        </ol>

        <hr class="my-8 border-slate-200">

        <h2 class="text-2xl font-bold text-scg-700 mt-10 mb-4">2. ภาพรวมขั้นตอนการทำงานของ Admin (Workflow)</h2>
        <p class="mb-4 text-slate-600">แผนภาพด้านล่างแสดงลำดับขั้นตอนการทำงานหลักที่ Admin ต้องดูแลในระบบ:</p>
        
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

        <hr class="my-8 border-slate-200">

        <h2 class="text-2xl font-bold text-scg-700 mt-10 mb-4">3. การจัดการผู้ใช้งาน (User Management)</h2>
        <p class="mb-4 text-slate-600">เมนูหลักสำหรับการจัดการพนักงานคือเมนู <strong>"⚙️ Admin"</strong> (มุมซ้ายล่างของหน้าจอ)</p>

        <h3 class="text-xl font-bold text-slate-700 mt-6 mb-3">3.1 การเพิ่มผู้ใช้งานใหม่ (Add User)</h3>
        <ol class="list-decimal pl-6 space-y-2 mb-6 text-slate-600">
            <li>ไปที่เมนู <strong>Admin</strong></li>
            <li>คลิกปุ่ม <strong>"+ Add New User"</strong> (เพิ่มผู้ใช้ใหม่)</li>
            <li>กรอกข้อมูลส่วนตัวของพนักงาน:
                <ul class="list-disc pl-6 mt-1 space-y-1">
                    <li><strong>รหัสพนักงาน (Employee ID / Username):</strong> ใช้สำหรับ Login</li>
                    <li><strong>รหัสผ่าน (Password):</strong> ตั้งรหัสผ่านเริ่มต้น</li>
                    <li><strong>ชื่อ-นามสกุล, ตำแหน่ง, ฝ่าย (Department), ฯลฯ</strong></li>
                </ul>
            </li>
            <li>เลือกระดับสิทธิ์ (Role):
                <ul class="list-disc pl-6 mt-1 space-y-1">
                    <li><code class="bg-slate-100 px-1 py-0.5 rounded text-scg-600">USER</code>: พนักงานทั่วไป ประเมินตนเองได้อย่างเดียว</li>
                    <li><code class="bg-slate-100 px-1 py-0.5 rounded text-scg-600">SUPERVISOR</code>: หัวหน้างาน สามารถประเมินลูกน้องได้</li>
                    <li><code class="bg-slate-100 px-1 py-0.5 rounded text-scg-600">ADMIN</code> / <code class="bg-slate-100 px-1 py-0.5 rounded text-scg-600">SUPER_ADMIN</code>: ผู้ดูแลระบบ</li>
                </ul>
            </li>
            <li><strong>(สำคัญ)</strong> หากตั้งให้เป็น <code class="bg-slate-100 px-1 py-0.5 rounded text-scg-600">ADMIN</code> หรือ <code class="bg-slate-100 px-1 py-0.5 rounded text-scg-600">SUPERVISOR</code> ระบบจะให้คุณระบุ <strong>Scope (ขอบเขตการดูแล)</strong> เช่น ให้ดูแลเฉพาะ Division: "Concrete Technology" เป็นต้น</li>
            <li>กดปุ่ม <strong>"Save"</strong> เพื่อบันทึกข้อมูล</li>
        </ol>

        <h3 class="text-xl font-bold text-slate-700 mt-6 mb-3">3.2 การแก้ไข / ลบ ผู้ใช้งาน</h3>
        <ul class="list-disc pl-6 space-y-2 mb-6 text-slate-600">
            <li><strong>การแก้ไข:</strong> ค้นหาชื่อพนักงานในตารางหน้า Admin แล้วคลิกปุ่ม <strong>"Edit" (ไอคอนดินสอ)</strong> เพื่อแก้ไขข้อมูล ตำแหน่ง หรือปรับเปลี่ยน Scope</li>
            <li><strong>การลบ:</strong> คลิกปุ่ม <strong>"Delete" (ไอคอนถังขยะ)</strong> ท้ายชื่อพนักงาน (ระบบจะถามเพื่อยืนยันก่อนลบเสมอ)</li>
        </ul>

        <div class="bg-red-50 border-l-4 border-red-500 p-4 my-4 rounded-r-lg">
            <div class="flex items-center">
                <i class="fa-solid fa-triangle-exclamation text-red-500 mr-2"></i>
                <strong class="text-red-700">ข้อควรระวัง (Warning)</strong>
            </div>
            <p class="text-red-600 mt-2 text-sm">การลบผู้ใช้งานจะทำให้ข้อมูลการประเมินของพนักงานคนนั้นหายไปจากระบบ หากพนักงานลาออก แนะนำให้ใช้วิธี <b>ระงับการใช้งาน (Inactive)</b> หากระบบมีรองรับ หรือเปลี่ยนรหัสผ่านเพื่อไม่ให้เข้าสู่ระบบได้แทน</p>
        </div>

        <hr class="my-8 border-slate-200">

        <h2 class="text-2xl font-bold text-scg-700 mt-10 mb-4">4. การติดตามการประเมิน (Evaluation Tracking)</h2>
        <p class="mb-4 text-slate-600">Admin มีหน้าที่สำคัญในการติดตามว่าพนักงานและหัวหน้างานดำเนินการประเมินครบถ้วนหรือไม่ โดยไปที่เมนู <strong>"ติดตามการประเมิน"</strong></p>

        <p class="font-bold text-slate-700 mb-2">สิ่งที่ Admin ต้องตรวจสอบ:</p>
        <ol class="list-decimal pl-6 space-y-2 mb-6 text-slate-600">
            <li><strong>คอลัมน์ "ประเมินตนเอง":</strong> หากมีวันที่แสดง แปลว่าพนักงานประเมินตนเองแล้ว</li>
            <li><strong>คอลัมน์ "ประเมิน(Before)":</strong> หากมีวันที่แสดง แปลว่าหัวหน้าได้ประเมินระดับทักษะก่อนการพัฒนาแล้ว</li>
            <li><strong>คอลัมน์ "ประเมิน(After)":</strong> หากมีวันที่แสดง แปลว่าหัวหน้าได้ประเมินระดับทักษะปัจจุบัน (Actual) แล้ว</li>
        </ol>

        <div class="bg-blue-50 border-l-4 border-blue-500 p-4 my-4 rounded-r-lg">
            <div class="flex items-center">
                <i class="fa-solid fa-lightbulb text-blue-500 mr-2"></i>
                <strong class="text-blue-700">คำแนะนำ (Tip)</strong>
            </div>
            <p class="text-blue-600 mt-2 text-sm">Admin สามารถกดปุ่ม <b>"Export Excel"</b> มุมขวาบน เพื่อดาวน์โหลดตารางติดตามการประเมินออกไปสรุปเป็นรายงานรายสัปดาห์/รายเดือน เพื่อติดตามทวงถามพนักงานที่ยังไม่ประเมินได้ทันที</p>
        </div>

        <hr class="my-8 border-slate-200">

        <h2 class="text-2xl font-bold text-scg-700 mt-10 mb-4">5. การวิเคราะห์ข้อมูลสำหรับ Admin (Data Analytics)</h2>
        <p class="mb-4 text-slate-600">เมื่อการประเมินเสร็จสิ้น Admin สามารถใช้ข้อมูลเพื่อวางแผนพัฒนาบุคลากรได้:</p>

        <ul class="list-disc pl-6 space-y-2 mb-6 text-slate-600">
            <li><strong>Dashboard:</strong> ดูภาพรวม Gap ของทักษะในหน่วยงาน และ Average Skill Level ของทีม เปรียบเทียบระหว่าง เป้าหมาย (Expected), ก่อนพัฒนา (Before), ประเมินตนเอง (Self), และปัจจุบัน (Actual)</li>
            <li><strong>Competency Analytic:</strong> วิเคราะห์พนักงานที่เป็น <strong>Top Performers</strong> (ผู้มีความพร้อมสูงสุด) และค้นหาทักษะที่เป็นจุดแข็งหรือจุดที่หน่วยงานต้องเร่งจัดอบรม</li>
            <li><strong>IDP (Individual Development Plan):</strong> เข้าไปดูแผนพัฒนารายบุคคลของพนักงานแต่ละคน เพื่อดูคอร์สเรียนแนะนำ (Training Need)</li>
        </ul>

        <div class="bg-amber-50 border-l-4 border-amber-500 p-4 my-4 rounded-r-lg">
            <div class="flex items-center">
                <i class="fa-solid fa-circle-info text-amber-500 mr-2"></i>
                <strong class="text-amber-700">หมายเหตุ (Note)</strong>
            </div>
            <p class="text-amber-600 mt-2 text-sm">คู่มือนี้เป็นคู่มือสรุปขั้นตอนการทำงานหลัก หากมีข้อสงสัยหรือพบ Error ในการใช้งาน สามารถติดต่อทีมงานผู้พัฒนาระบบเพื่อแก้ไขได้ตลอดเวลา</p>
        </div>
    </div>
</section>
"""
    content = content.replace('</main>', manual_content + '\n\n</main>')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Patched {filepath}")

inject_manual_tab('static/index.html')
inject_manual_tab('index_render.html')
