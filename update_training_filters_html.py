import re

html_path = 'd:\\Work\\งานใหม่\\อบรม\\2026\\Vibe Coding Workshop\\Project\\competency_system_dynamic_rbac_hierarchy.html'

with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace grid-cols-2 with grid-cols-4
content = content.replace('md:grid-cols-2 gap-6 relative z-20">', 'md:grid-cols-4 gap-6 relative z-20">')

# Rename "Positions" to "Position Name"
content = content.replace('กรองตามตำแหน่ง (Positions)', 'กรองตามตำแหน่ง (Position Name)')

# Add new filters after the pos-dropdown-menu block
new_filters = """
                    <div class="w-full relative">
                        <label class="block text-sm font-bold text-slate-700 mb-2"><i class="fa-solid fa-filter text-scg-500 mr-1"></i> กรองตาม Section</label>
                        <button onclick="toggleFilterMenu('section-dropdown-menu')" class="w-full flex items-center justify-between bg-white border border-slate-300 px-4 py-2.5 rounded-xl text-left shadow-sm hover:bg-slate-50 focus:outline-none focus:ring-2 focus:ring-scg-500 transition-colors">
                            <span class="text-sm font-medium text-slate-700 truncate" id="section-dropdown-text">เลือก Section ทั้งหมด</span>
                            <i class="fa-solid fa-chevron-down text-slate-400 ml-2"></i>
                        </button>
                        <div id="section-dropdown-menu" class="filter-menu hidden absolute top-full left-0 w-full mt-2 bg-white border border-slate-200 rounded-xl shadow-xl z-30 max-h-64 overflow-y-auto">
                            <div id="section-filters" class="p-2 flex flex-col gap-1">
                                <!-- Injected by JS -->
                            </div>
                        </div>
                    </div>

                    <div class="w-full relative">
                        <label class="block text-sm font-bold text-slate-700 mb-2"><i class="fa-solid fa-filter text-scg-500 mr-1"></i> กรองตาม Department</label>
                        <button onclick="toggleFilterMenu('department-dropdown-menu')" class="w-full flex items-center justify-between bg-white border border-slate-300 px-4 py-2.5 rounded-xl text-left shadow-sm hover:bg-slate-50 focus:outline-none focus:ring-2 focus:ring-scg-500 transition-colors">
                            <span class="text-sm font-medium text-slate-700 truncate" id="department-dropdown-text">เลือก Department ทั้งหมด</span>
                            <i class="fa-solid fa-chevron-down text-slate-400 ml-2"></i>
                        </button>
                        <div id="department-dropdown-menu" class="filter-menu hidden absolute top-full left-0 w-full mt-2 bg-white border border-slate-200 rounded-xl shadow-xl z-30 max-h-64 overflow-y-auto">
                            <div id="department-filters" class="p-2 flex flex-col gap-1">
                                <!-- Injected by JS -->
                            </div>
                        </div>
                    </div>

                    <div class="w-full relative">
                        <label class="block text-sm font-bold text-slate-700 mb-2"><i class="fa-solid fa-filter text-scg-500 mr-1"></i> กรองตาม Sub1-Division</label>
                        <button onclick="toggleFilterMenu('sub1division-dropdown-menu')" class="w-full flex items-center justify-between bg-white border border-slate-300 px-4 py-2.5 rounded-xl text-left shadow-sm hover:bg-slate-50 focus:outline-none focus:ring-2 focus:ring-scg-500 transition-colors">
                            <span class="text-sm font-medium text-slate-700 truncate" id="sub1division-dropdown-text">เลือก Sub1-Division ทั้งหมด</span>
                            <i class="fa-solid fa-chevron-down text-slate-400 ml-2"></i>
                        </button>
                        <div id="sub1division-dropdown-menu" class="filter-menu hidden absolute top-full left-0 w-full mt-2 bg-white border border-slate-200 rounded-xl shadow-xl z-30 max-h-64 overflow-y-auto">
                            <div id="sub1division-filters" class="p-2 flex flex-col gap-1">
                                <!-- Injected by JS -->
                            </div>
                        </div>
                    </div>

                    <div class="w-full relative">
                        <label class="block text-sm font-bold text-slate-700 mb-2"><i class="fa-solid fa-filter text-scg-500 mr-1"></i> กรองตาม Division</label>
                        <button onclick="toggleFilterMenu('division-dropdown-menu')" class="w-full flex items-center justify-between bg-white border border-slate-300 px-4 py-2.5 rounded-xl text-left shadow-sm hover:bg-slate-50 focus:outline-none focus:ring-2 focus:ring-scg-500 transition-colors">
                            <span class="text-sm font-medium text-slate-700 truncate" id="division-dropdown-text">เลือก Division ทั้งหมด</span>
                            <i class="fa-solid fa-chevron-down text-slate-400 ml-2"></i>
                        </button>
                        <div id="division-dropdown-menu" class="filter-menu hidden absolute top-full left-0 w-full mt-2 bg-white border border-slate-200 rounded-xl shadow-xl z-30 max-h-64 overflow-y-auto">
                            <div id="division-filters" class="p-2 flex flex-col gap-1">
                                <!-- Injected by JS -->
                            </div>
                        </div>
                    </div>

                    <div class="w-full relative">
                        <label class="block text-sm font-bold text-slate-700 mb-2"><i class="fa-solid fa-filter text-scg-500 mr-1"></i> กรองตาม Sub1-Company</label>
                        <button onclick="toggleFilterMenu('sub1company-dropdown-menu')" class="w-full flex items-center justify-between bg-white border border-slate-300 px-4 py-2.5 rounded-xl text-left shadow-sm hover:bg-slate-50 focus:outline-none focus:ring-2 focus:ring-scg-500 transition-colors">
                            <span class="text-sm font-medium text-slate-700 truncate" id="sub1company-dropdown-text">เลือก Sub1-Company ทั้งหมด</span>
                            <i class="fa-solid fa-chevron-down text-slate-400 ml-2"></i>
                        </button>
                        <div id="sub1company-dropdown-menu" class="filter-menu hidden absolute top-full left-0 w-full mt-2 bg-white border border-slate-200 rounded-xl shadow-xl z-30 max-h-64 overflow-y-auto">
                            <div id="sub1company-filters" class="p-2 flex flex-col gap-1">
                                <!-- Injected by JS -->
                            </div>
                        </div>
                    </div>

                    <div class="w-full relative">
                        <label class="block text-sm font-bold text-slate-700 mb-2"><i class="fa-solid fa-filter text-scg-500 mr-1"></i> กรองตาม Company</label>
                        <button onclick="toggleFilterMenu('company-dropdown-menu')" class="w-full flex items-center justify-between bg-white border border-slate-300 px-4 py-2.5 rounded-xl text-left shadow-sm hover:bg-slate-50 focus:outline-none focus:ring-2 focus:ring-scg-500 transition-colors">
                            <span class="text-sm font-medium text-slate-700 truncate" id="company-dropdown-text">เลือก Company ทั้งหมด</span>
                            <i class="fa-solid fa-chevron-down text-slate-400 ml-2"></i>
                        </button>
                        <div id="company-dropdown-menu" class="filter-menu hidden absolute top-full left-0 w-full mt-2 bg-white border border-slate-200 rounded-xl shadow-xl z-30 max-h-64 overflow-y-auto">
                            <div id="company-filters" class="p-2 flex flex-col gap-1">
                                <!-- Injected by JS -->
                            </div>
                        </div>
                    </div>
"""

# Find the end of pos-dropdown-menu block
target_str = """                        <div id="pos-dropdown-menu" class="filter-menu hidden absolute top-full left-0 w-full mt-2 bg-white border border-slate-200 rounded-xl shadow-xl z-30 max-h-64 overflow-y-auto">
                            <div id="position-filters" class="p-2 flex flex-col gap-1">
                                <!-- Injected by JS -->
                            </div>
                        </div>
                    </div>"""

if target_str in content:
    content = content.replace(target_str, target_str + new_filters)
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated HTML successfully.")
else:
    print("Could not find target block to inject new filters.")
