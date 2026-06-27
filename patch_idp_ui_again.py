import re

def patch_idp_html(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # The block we want to replace starts with:
    # <div class="absolute top-6 right-6 text-right">
    # and ends with:
    # <div class="w-full h-[400px] mt-16 lg:mt-10">
    # and has "% Completed Skill Level" in the middle.
    
    # Let's use a regex to match the block
    pattern = r'(<div class="absolute top-6 right-6 text-right">.*?</div\s*>\s*</div\s*>)\s*(<div class="w-full h-\[400px\] mt-16 lg:mt-10">)'
    
    def replacer(match):
        header_block = match.group(1)
        # We need to inject the filter dropdown inside the header_block before the closing </div></div>
        
        filter_ui = """                            
                            <div class="w-full max-w-xs text-left mt-2 inline-block">
                                <label class="block text-[10px] font-bold text-slate-500 mb-1">แสดงข้อมูล (Filter)</label>
                                <div class="relative filter-dropdown">
                                    <div class="w-full px-3 py-1.5 border border-slate-200 rounded-lg text-xs bg-white flex justify-between items-center cursor-pointer hover:bg-slate-50 transition-colors" onclick="this.nextElementSibling.classList.toggle('hidden');">
                                        <span class="text-slate-600">แสดงทั้งหมด</span>
                                        <i class="fa-solid fa-chevron-down text-[10px] text-slate-400"></i>
                                    </div>
                                    <div class="absolute top-full left-0 right-0 mt-1 bg-white border border-slate-100 rounded-lg shadow-xl z-[60] hidden p-2">
                                        <label class="flex items-center gap-2 p-1.5 hover:bg-slate-50 rounded cursor-pointer text-xs">
                                            <input type="checkbox" checked value="target" onchange="toggleRadarFilter(this, 'idp')" class="w-3.5 h-3.5 rounded text-scg-600 border-slate-300 focus:ring-scg-500"> Target
                                        </label>
                                        <label class="flex items-center gap-2 p-1.5 hover:bg-slate-50 rounded cursor-pointer text-xs">
                                            <input type="checkbox" checked value="before" onchange="toggleRadarFilter(this, 'idp')" class="w-3.5 h-3.5 rounded text-purple-500 border-slate-300 focus:ring-purple-500"> Before
                                        </label>
                                        <label class="flex items-center gap-2 p-1.5 hover:bg-slate-50 rounded cursor-pointer text-xs">
                                            <input type="checkbox" checked value="self" onchange="toggleRadarFilter(this, 'idp')" class="w-3.5 h-3.5 rounded text-amber-500 border-slate-300 focus:ring-amber-500"> Self Eva.
                                        </label>
                                        <label class="flex items-center gap-2 p-1.5 hover:bg-slate-50 rounded cursor-pointer text-xs">
                                            <input type="checkbox" checked value="actual" onchange="toggleRadarFilter(this, 'idp')" class="w-3.5 h-3.5 rounded text-red-600 border-slate-300 focus:ring-red-600"> Actual
                                        </label>
                                    </div>
                                </div>
                            </div>
"""
        
        # Modify the header_block to add the filter_ui before the final </div>
        # Actually header_block looks like:
        # <div class="absolute top-6 right-6 text-right">
        #    ...
        # </div>
        
        # Let's just reconstruct it
        new_header_block = header_block.replace('class="absolute top-6 right-6 text-right"', 'class="absolute top-6 right-6 text-right w-full sm:w-1/2 flex flex-col items-end"')
        # Insert filter_ui right before the last </div>
        last_div_idx = new_header_block.rfind('</div>')
        new_header_block = new_header_block[:last_div_idx] + filter_ui + new_header_block[last_div_idx:]
        
        return new_header_block + '\n                        <div class="w-full h-[400px] mt-32 lg:mt-32">'
        
    new_content, count = re.subn(pattern, replacer, content, flags=re.DOTALL)
    if count > 0:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Successfully patched IDP HTML in {filepath}")
    else:
        print(f"Failed to find pattern in {filepath}")

patch_idp_html('static/index.html')
patch_idp_html('index_render.html')
