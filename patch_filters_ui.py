import re

files = [
    'd:/Work/งานใหม่/อบรม/2026/Vibe Coding Workshop/Project/competency-system/static/index.html',
    'd:/Work/งานใหม่/อบรม/2026/Vibe Coding Workshop/Project/competency-system/index_render.html'
]

replacement = """<div class="flex flex-col xl:flex-row gap-6">
                        <!-- Hierarchy Group -->
                        <div class="xl:w-3/4 bg-slate-50 border border-slate-200 rounded-xl p-4">
                            <h4 class="text-sm font-bold text-slate-700 mb-4 border-b border-slate-200 pb-2"><i class="fa-solid fa-sitemap text-scg-500 mr-2"></i> โครงสร้างองค์กรและบุคลากร (Hierarchy)</h4>
                            <div class="grid grid-cols-1 md:grid-cols-3 xl:grid-cols-4 gap-4">
                                <div class="w-full relative">
                                    <label class="block text-sm font-bold text-slate-700 mb-2"><i class="fa-solid fa-layer-group text-scg-500 mr-1"></i> กรองตามกลุ่มงาน (Job Groups)</label>
                                    <button onclick="toggleFilterMenu('job-group-menu')" class="w-full flex items-center justify-between bg-white border border-slate-300 px-4 py-2.5 rounded-xl text-left shadow-sm hover:bg-slate-50 focus:outline-none focus:ring-2 focus:ring-scg-500 transition-colors">
                                        <span class="text-sm font-medium text-slate-700 truncate" id="job-group-dropdown-text">เลือกกลุ่มงานทั้งหมด</span>
                                        <i class="fa-solid fa-chevron-down text-slate-400 ml-2"></i>
                                    </button>
                                    <div id="job-group-menu" class="filter-menu hidden absolute top-full left-0 w-full mt-2 bg-white border border-slate-200 rounded-xl shadow-xl z-30 max-h-64 overflow-y-auto">
                                        <div id="job-group-filters" class="p-2 flex flex-col gap-1"></div>
                                    </div>
                                </div>

                                <div class="w-full relative">
                                    <label class="block text-sm font-bold text-slate-700 mb-2"><i class="fa-solid fa-filter text-scg-500 mr-1"></i> กรองตามตำแหน่ง (Position Name)</label>
                                    <button onclick="toggleFilterMenu('pos-dropdown-menu')" class="w-full flex items-center justify-between bg-white border border-slate-300 px-4 py-2.5 rounded-xl text-left shadow-sm hover:bg-slate-50 focus:outline-none focus:ring-2 focus:ring-scg-500 transition-colors">
                                        <span class="text-sm font-medium text-slate-700 truncate" id="pos-dropdown-text">เลือกตำแหน่งทั้งหมด</span>
                                        <i class="fa-solid fa-chevron-down text-slate-400 ml-2"></i>
                                    </button>
                                    <div id="pos-dropdown-menu" class="filter-menu hidden absolute top-full left-0 w-full mt-2 bg-white border border-slate-200 rounded-xl shadow-xl z-30 max-h-64 overflow-y-auto">
                                        <div id="position-filters" class="p-2 flex flex-col gap-1"></div>
                                    </div>
                                </div>

                                <div class="w-full relative">
                                    <label class="block text-sm font-bold text-slate-700 mb-2"><i class="fa-solid fa-filter text-scg-500 mr-1"></i> กรองตาม Section</label>
                                    <button onclick="toggleFilterMenu('section-dropdown-menu')" class="w-full flex items-center justify-between bg-white border border-slate-300 px-4 py-2.5 rounded-xl text-left shadow-sm hover:bg-slate-50 focus:outline-none focus:ring-2 focus:ring-scg-500 transition-colors">
                                        <span class="text-sm font-medium text-slate-700 truncate" id="section-dropdown-text">เลือก Section ทั้งหมด</span>
                                        <i class="fa-solid fa-chevron-down text-slate-400 ml-2"></i>
                                    </button>
                                    <div id="section-dropdown-menu" class="filter-menu hidden absolute top-full left-0 w-full mt-2 bg-white border border-slate-200 rounded-xl shadow-xl z-30 max-h-64 overflow-y-auto">
                                        <div id="section-filters" class="p-2 flex flex-col gap-1"></div>
                                    </div>
                                </div>

                                <div class="w-full relative">
                                    <label class="block text-sm font-bold text-slate-700 mb-2"><i class="fa-solid fa-filter text-scg-500 mr-1"></i> กรองตาม Department</label>
                                    <button onclick="toggleFilterMenu('department-dropdown-menu')" class="w-full flex items-center justify-between bg-white border border-slate-300 px-4 py-2.5 rounded-xl text-left shadow-sm hover:bg-slate-50 focus:outline-none focus:ring-2 focus:ring-scg-500 transition-colors">
                                        <span class="text-sm font-medium text-slate-700 truncate" id="department-dropdown-text">เลือก Department ทั้งหมด</span>
                                        <i class="fa-solid fa-chevron-down text-slate-400 ml-2"></i>
                                    </button>
                                    <div id="department-dropdown-menu" class="filter-menu hidden absolute top-full left-0 w-full mt-2 bg-white border border-slate-200 rounded-xl shadow-xl z-30 max-h-64 overflow-y-auto">
                                        <div id="department-filters" class="p-2 flex flex-col gap-1"></div>
                                    </div>
                                </div>

                                <div class="w-full relative">
                                    <label class="block text-sm font-bold text-slate-700 mb-2"><i class="fa-solid fa-filter text-scg-500 mr-1"></i> กรองตาม Sub1-Division</label>
                                    <button onclick="toggleFilterMenu('sub1division-dropdown-menu')" class="w-full flex items-center justify-between bg-white border border-slate-300 px-4 py-2.5 rounded-xl text-left shadow-sm hover:bg-slate-50 focus:outline-none focus:ring-2 focus:ring-scg-500 transition-colors">
                                        <span class="text-sm font-medium text-slate-700 truncate" id="sub1division-dropdown-text">เลือก Sub1-Division ทั้งหมด</span>
                                        <i class="fa-solid fa-chevron-down text-slate-400 ml-2"></i>
                                    </button>
                                    <div id="sub1division-dropdown-menu" class="filter-menu hidden absolute top-full left-0 w-full mt-2 bg-white border border-slate-200 rounded-xl shadow-xl z-30 max-h-64 overflow-y-auto">
                                        <div id="sub1division-filters" class="p-2 flex flex-col gap-1"></div>
                                    </div>
                                </div>

                                <div class="w-full relative">
                                    <label class="block text-sm font-bold text-slate-700 mb-2"><i class="fa-solid fa-filter text-scg-500 mr-1"></i> กรองตาม Division</label>
                                    <button onclick="toggleFilterMenu('division-dropdown-menu')" class="w-full flex items-center justify-between bg-white border border-slate-300 px-4 py-2.5 rounded-xl text-left shadow-sm hover:bg-slate-50 focus:outline-none focus:ring-2 focus:ring-scg-500 transition-colors">
                                        <span class="text-sm font-medium text-slate-700 truncate" id="division-dropdown-text">เลือก Division ทั้งหมด</span>
                                        <i class="fa-solid fa-chevron-down text-slate-400 ml-2"></i>
                                    </button>
                                    <div id="division-dropdown-menu" class="filter-menu hidden absolute top-full left-0 w-full mt-2 bg-white border border-slate-200 rounded-xl shadow-xl z-30 max-h-64 overflow-y-auto">
                                        <div id="division-filters" class="p-2 flex flex-col gap-1"></div>
                                    </div>
                                </div>

                                <div class="w-full relative">
                                    <label class="block text-sm font-bold text-slate-700 mb-2"><i class="fa-solid fa-filter text-scg-500 mr-1"></i> กรองตาม Sub1-Company</label>
                                    <button onclick="toggleFilterMenu('sub1company-dropdown-menu')" class="w-full flex items-center justify-between bg-white border border-slate-300 px-4 py-2.5 rounded-xl text-left shadow-sm hover:bg-slate-50 focus:outline-none focus:ring-2 focus:ring-scg-500 transition-colors">
                                        <span class="text-sm font-medium text-slate-700 truncate" id="sub1company-dropdown-text">เลือก Sub1-Company ทั้งหมด</span>
                                        <i class="fa-solid fa-chevron-down text-slate-400 ml-2"></i>
                                    </button>
                                    <div id="sub1company-dropdown-menu" class="filter-menu hidden absolute top-full left-0 w-full mt-2 bg-white border border-slate-200 rounded-xl shadow-xl z-30 max-h-64 overflow-y-auto">
                                        <div id="sub1company-filters" class="p-2 flex flex-col gap-1"></div>
                                    </div>
                                </div>

                                <div class="w-full relative">
                                    <label class="block text-sm font-bold text-slate-700 mb-2"><i class="fa-solid fa-filter text-scg-500 mr-1"></i> กรองตาม Company</label>
                                    <button onclick="toggleFilterMenu('company-dropdown-menu')" class="w-full flex items-center justify-between bg-white border border-slate-300 px-4 py-2.5 rounded-xl text-left shadow-sm hover:bg-slate-50 focus:outline-none focus:ring-2 focus:ring-scg-500 transition-colors">
                                        <span class="text-sm font-medium text-slate-700 truncate" id="company-dropdown-text">เลือก Company ทั้งหมด</span>
                                        <i class="fa-solid fa-chevron-down text-slate-400 ml-2"></i>
                                    </button>
                                    <div id="company-dropdown-menu" class="filter-menu hidden absolute top-full left-0 w-full mt-2 bg-white border border-slate-200 rounded-xl shadow-xl z-30 max-h-64 overflow-y-auto">
                                        <div id="company-filters" class="p-2 flex flex-col gap-1"></div>
                                    </div>
                                </div>

                                <div class="w-full relative">
                                    <label class="block text-sm font-bold text-slate-700 mb-2"><i class="fa-solid fa-user text-scg-500 mr-1"></i> ชื่อพนักงาน</label>
                                    <button onclick="toggleFilterMenu('employee-menu')" class="w-full flex items-center justify-between bg-white border border-slate-300 px-4 py-2.5 rounded-xl text-left shadow-sm hover:bg-slate-50 focus:outline-none focus:ring-2 focus:ring-scg-500 transition-colors">
                                        <span class="text-sm font-medium text-slate-700 truncate" id="employee-dropdown-text">เลือกพนักงานทั้งหมด</span>
                                        <i class="fa-solid fa-chevron-down text-slate-400 ml-2"></i>
                                    </button>
                                    <div id="employee-menu" class="filter-menu hidden absolute top-full left-0 w-full mt-2 bg-white border border-slate-200 rounded-xl shadow-xl z-30 max-h-64 overflow-y-auto">
                                        <div id="employee-filters" class="p-2 flex flex-col gap-1"></div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Competency Group -->
                        <div class="xl:w-1/4 bg-scg-50/50 border border-scg-100 rounded-xl p-4">
                            <h4 class="text-sm font-bold text-scg-700 mb-4 border-b border-scg-100 pb-2"><i class="fa-solid fa-star text-scg-500 mr-2"></i> ทักษะความคาดหวัง (Competency)</h4>
                            <div class="grid grid-cols-1 gap-4">
                                <div class="w-full relative filter-dropdown-container">
                                    <label class="block text-sm font-bold text-slate-700 mb-2"><i class="fa-solid fa-layer-group text-scg-500 mr-1"></i> กลุ่ม Competency</label>
                                    <button onclick="toggleFilterMenu('comp-group-menu')" class="w-full flex items-center justify-between bg-white border border-slate-300 px-4 py-2.5 rounded-xl text-left shadow-sm hover:bg-slate-50 focus:outline-none focus:ring-2 focus:ring-scg-500 transition-colors">
                                        <span class="text-sm font-medium text-slate-700 truncate" id="comp-group-dropdown-text">เลือกกลุ่มทักษะทั้งหมด</span>
                                        <i class="fa-solid fa-chevron-down text-slate-400 ml-2"></i>
                                    </button>
                                    <div id="comp-group-menu" class="filter-menu hidden absolute top-full left-0 w-full mt-2 bg-white border border-slate-200 rounded-xl shadow-xl z-30 max-h-64 overflow-y-auto">
                                        <div id="comp-group-filters" class="p-2 flex flex-col gap-1"></div>
                                    </div>
                                </div>

                                <div class="w-full relative filter-dropdown-container">
                                    <label class="block text-sm font-bold text-slate-700 mb-2"><i class="fa-solid fa-filter text-scg-500 mr-1"></i> หัวข้อ Competency</label>
                                    <button onclick="toggleFilterMenu('comp-dropdown-menu')" class="w-full flex items-center justify-between bg-white border border-slate-300 px-4 py-2.5 rounded-xl text-left shadow-sm hover:bg-slate-50 focus:outline-none focus:ring-2 focus:ring-scg-500 transition-colors">
                                        <span class="text-sm font-medium text-slate-700 truncate" id="comp-dropdown-text">เลือกทักษะทั้งหมด</span>
                                        <i class="fa-solid fa-chevron-down text-slate-400 ml-2"></i>
                                    </button>
                                    <div id="comp-dropdown-menu" class="filter-menu hidden absolute top-full left-0 w-full mt-2 bg-white border border-slate-200 rounded-xl shadow-xl z-30 max-h-64 overflow-y-auto">
                                        <div id="competency-filters" class="p-2 flex flex-col gap-1"></div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>"""

for file_path in files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # We find the start and end of the old grid container
    start_pattern = r'<div class="grid grid-cols-1 md:grid-cols-5 gap-4">\s*<div class="w-full relative">'
    end_pattern = r'<!-- Injected by JS -->\s*</div>\s*</div>\s*</div>\s*</div>'
    
    # Using re.search to find the block
    match_start = re.search(start_pattern, content)
    match_end = re.search(end_pattern, content)
    
    if match_start and match_end:
        start_idx = match_start.start()
        end_idx = match_end.end()
        # Ensure it's the correct block
        if "comp-dropdown-menu" in content[start_idx:end_idx]:
            new_content = content[:start_idx] + replacement + content[end_idx:]
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Patched {file_path}")
        else:
            print(f"Warning: Block not identified correctly in {file_path}")
    else:
        print(f"Warning: Start or End pattern not found in {file_path}")

print("Done")
