import re

def fix_all(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Fix IDP
    pattern_idp = r"""(<div class="w-full max-w-xs text-left mt-2 inline-block">.*?)(<span.*?)(>แสดงทั้งหมด</span>)(.*?)(toggleRadarFilter\(this,\s*'idp'\))(.*?)(toggleRadarFilter\(this,\s*'idp'\))(.*?)(toggleRadarFilter\(this,\s*'idp'\))(.*?)(toggleRadarFilter\(this,\s*'idp'\))(.*?</div>\s*</div>\s*</div>)"""
    
    def repl_idp(m):
        return m.group(1) + '<span id="idp-radar-filter-text" class="text-slate-600"' + m.group(3) + \
               m.group(4).replace('class="', 'class="idp-radar-cb ') + "updateRadarFilter('idp')" + \
               m.group(6).replace('class="', 'class="idp-radar-cb ') + "updateRadarFilter('idp')" + \
               m.group(8).replace('class="', 'class="idp-radar-cb ') + "updateRadarFilter('idp')" + \
               m.group(10).replace('class="', 'class="idp-radar-cb ') + "updateRadarFilter('idp')" + \
               m.group(12)
    
    content, c_idp = re.subn(pattern_idp, repl_idp, content, flags=re.DOTALL)

    # 2. Fix Analytic
    pattern_ana = r"""(<div class="w-full sm:w-64">.*?)(<span.*?)(>แสดงทั้งหมด</span>)(.*?)(toggleRadarFilter\(this,\s*'analytic'\);\s*renderAnalyticTab\(\);?)(.*?)(toggleRadarFilter\(this,\s*'analytic'\);\s*renderAnalyticTab\(\);?)(.*?)(toggleRadarFilter\(this,\s*'analytic'\);\s*renderAnalyticTab\(\);?)(.*?)(toggleRadarFilter\(this,\s*'analytic'\);\s*renderAnalyticTab\(\);?)(.*?</div>\s*</div>\s*</div>)"""
    
    def repl_ana(m):
        return m.group(1) + '<span id="analytic-radar-filter-text" class="text-slate-600"' + m.group(3) + \
               m.group(4).replace('class="', 'class="analytic-radar-cb ') + "updateRadarFilter('analytic')" + \
               m.group(6).replace('class="', 'class="analytic-radar-cb ') + "updateRadarFilter('analytic')" + \
               m.group(8).replace('class="', 'class="analytic-radar-cb ') + "updateRadarFilter('analytic')" + \
               m.group(10).replace('class="', 'class="analytic-radar-cb ') + "updateRadarFilter('analytic')" + \
               m.group(12)
               
    content, c_ana = re.subn(pattern_ana, repl_ana, content, flags=re.DOTALL)

    # 3. Fix updateRadarFilter for IDP
    content = content.replace(
        "if (type === 'idp') drawIDPRadar();",
        "if (type === 'idp') { if (typeof renderIDPContent === 'function') renderIDPContent(); }"
    )
    
    # 4. Fix dropdown IDs for click outside
    content = content.replace(
        """<div class="absolute top-full left-0 right-0 mt-1 bg-white border border-slate-100 rounded-lg shadow-xl z-[60] hidden p-2">""",
        """<div class="radar-dropdown absolute top-full left-0 right-0 mt-1 bg-white border border-slate-100 rounded-lg shadow-xl z-[60] hidden p-2">"""
    )
    # The click outside logic uses `getElementById(`${type}-radar-filter-dropdown`)`
    # We should add the id.
    
    # Let's fix the dropdown IDs explicitly
    def repl_idp_dropdown(m):
        return m.group(0).replace('class="absolute', 'id="idp-radar-filter-dropdown" class="absolute')
    
    def repl_ana_dropdown(m):
        return m.group(0).replace('class="absolute', 'id="analytic-radar-filter-dropdown" class="absolute')
        
    content = re.sub(r'(<div class="w-full max-w-xs text-left mt-2 inline-block">.*?)(<div class="absolute top-full)', repl_idp_dropdown, content, flags=re.DOTALL)
    content = re.sub(r'(<div class="w-full sm:w-64">.*?)(<div class="absolute top-full)', repl_ana_dropdown, content, flags=re.DOTALL)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Patched {filepath}, IDP:{c_idp}, Ana:{c_ana}")

fix_all('static/index.html')
fix_all('index_render.html')
