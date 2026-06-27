import re

def patch_analytic_html(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # The block we want to replace starts with:
    # <div class="mb-6 flex justify-between items-end">
    #     <div>
    #         <h2 class="text-2xl font-bold text-scg-900">Competency Analytic</h2>
    
    pattern = r'(<div class="mb-6 flex justify-between items-end">[\s\n]*<div>[\s\n]*<h2 class="text-2xl font-bold text-scg-900">Competency Analytic</h2>[\s\n]*<p class="text-slate-500 text-sm">.*?</p>[\s\n]*</div>)'
    
    def replacer(match):
        header_block = match.group(1)
        
        filter_ui = """
                    <div class="w-full sm:w-64">
                        <label class="block text-[10px] font-bold text-slate-500 mb-1">แสดงข้อมูล (Filter)</label>
                        <div class="relative filter-dropdown">
                            <div class="w-full px-3 py-1.5 border border-slate-200 rounded-lg text-xs bg-white flex justify-between items-center cursor-pointer hover:bg-slate-50 transition-colors" onclick="this.nextElementSibling.classList.toggle('hidden');">
                                <span class="text-slate-600">แสดงทั้งหมด</span>
                                <i class="fa-solid fa-chevron-down text-[10px] text-slate-400"></i>
                            </div>
                            <div class="absolute top-full left-0 right-0 mt-1 bg-white border border-slate-100 rounded-lg shadow-xl z-[60] hidden p-2">
                                <label class="flex items-center gap-2 p-1.5 hover:bg-slate-50 rounded cursor-pointer text-xs">
                                    <input type="checkbox" checked value="target" onchange="toggleRadarFilter(this, 'analytic'); renderAnalyticTab();" class="w-3.5 h-3.5 rounded text-scg-600 border-slate-300 focus:ring-scg-500"> Target
                                </label>
                                <label class="flex items-center gap-2 p-1.5 hover:bg-slate-50 rounded cursor-pointer text-xs">
                                    <input type="checkbox" checked value="before" onchange="toggleRadarFilter(this, 'analytic'); renderAnalyticTab();" class="w-3.5 h-3.5 rounded text-purple-500 border-slate-300 focus:ring-purple-500"> Before
                                </label>
                                <label class="flex items-center gap-2 p-1.5 hover:bg-slate-50 rounded cursor-pointer text-xs">
                                    <input type="checkbox" checked value="self" onchange="toggleRadarFilter(this, 'analytic'); renderAnalyticTab();" class="w-3.5 h-3.5 rounded text-amber-500 border-slate-300 focus:ring-amber-500"> Self Eva.
                                </label>
                                <label class="flex items-center gap-2 p-1.5 hover:bg-slate-50 rounded cursor-pointer text-xs">
                                    <input type="checkbox" checked value="actual" onchange="toggleRadarFilter(this, 'analytic'); renderAnalyticTab();" class="w-3.5 h-3.5 rounded text-red-600 border-slate-300 focus:ring-red-600"> Actual
                                </label>
                            </div>
                        </div>
                    </div>"""
        
        return header_block + filter_ui
        
    new_content, count = re.subn(pattern, replacer, content)
    if count > 0:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Successfully patched Analytic HTML in {filepath}")
    else:
        print(f"Failed to find pattern in {filepath}")

patch_analytic_html('static/index.html')
patch_analytic_html('index_render.html')
