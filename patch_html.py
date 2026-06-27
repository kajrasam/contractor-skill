import os

modal_html = '''
    <!-- Manage Admins Modal -->
    <div id="manage-admins-modal" class="fixed inset-0 bg-slate-900/50 backdrop-blur-sm z-50 hidden flex items-center justify-center">
        <div class="bg-white rounded-2xl w-full max-w-4xl max-h-[90vh] flex flex-col shadow-xl overflow-hidden">
            <div class="p-6 border-b border-slate-100 bg-slate-50 flex justify-between items-center">
                <h3 class="text-xl font-bold text-slate-800"><i class="fa-solid fa-users-cog text-purple-600 mr-2"></i>จัดการ Admin (Super Admin)</h3>
                <button onclick="document.getElementById('manage-admins-modal').classList.add('hidden')" class="text-slate-400 hover:text-slate-600 transition-colors">
                    <i class="fa-solid fa-xmark text-xl"></i>
                </button>
            </div>
            <div class="p-6 overflow-y-auto flex-1 custom-scrollbar">
                <!-- Add New Admin Form -->
                <div class="bg-slate-50 p-4 rounded-xl border border-slate-200 mb-6">
                    <h4 class="font-bold text-slate-700 mb-4">เพิ่ม/แก้ไข Admin</h4>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                            <label class="block text-xs font-bold text-slate-500 mb-1">Username (ID)</label>
                            <input type="text" id="admin-uid" class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm bg-white">
                        </div>
                        <div>
                            <label class="block text-xs font-bold text-slate-500 mb-1">Password</label>
                            <input type="text" id="admin-pass" class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm bg-white">
                        </div>
                        <div>
                            <label class="block text-xs font-bold text-slate-500 mb-1">Name</label>
                            <input type="text" id="admin-name" class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm bg-white">
                        </div>
                        <div>
                            <label class="block text-xs font-bold text-slate-500 mb-1">Scope Section</label>
                            <input type="text" id="admin-scope-sec" placeholder="ALL หรือ ชื่อ Section" class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm bg-white">
                        </div>
                        <div>
                            <label class="block text-xs font-bold text-slate-500 mb-1">Scope Department</label>
                            <input type="text" id="admin-scope-dep" placeholder="ALL หรือ ชื่อ Department" class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm bg-white">
                        </div>
                    </div>
                    <div class="mt-4 flex justify-end gap-2">
                        <button onclick="clearAdminForm()" class="px-4 py-2 text-sm font-bold text-slate-600 bg-white border border-slate-300 rounded-lg hover:bg-slate-50">Clear</button>
                        <button onclick="saveAdminUser()" class="px-4 py-2 text-sm font-bold text-white bg-purple-600 rounded-lg hover:bg-purple-700 shadow-sm">Save Admin</button>
                    </div>
                </div>

                <!-- Admin List -->
                <h4 class="font-bold text-slate-700 mb-4">รายชื่อ Admin ทั้งหมด</h4>
                <div class="overflow-x-auto rounded-xl border border-slate-200">
                    <table class="w-full text-left border-collapse text-sm">
                        <thead class="bg-slate-50">
                            <tr class="text-slate-600 font-bold border-b border-slate-200">
                                <th class="py-3 px-4">ID</th>
                                <th class="py-3 px-4">Name</th>
                                <th class="py-3 px-4">Section Scope</th>
                                <th class="py-3 px-4">Dept Scope</th>
                                <th class="py-3 px-4 text-center">Actions</th>
                            </tr>
                        </thead>
                        <tbody id="admin-users-table-body" class="bg-white divide-y divide-slate-100">
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
'''

def insert_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'id="manage-admins-modal"' in content:
        return
        
    target = '<div id="add-employee-modal"'
    new_content = content.replace(target, modal_html + '\n    ' + target)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

insert_html('index_render.html')
insert_html('static/index.html')
print('Modal HTML inserted.')
