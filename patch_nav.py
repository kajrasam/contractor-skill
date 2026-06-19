import sys
with open('build_frontend.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace all occurrences of nav-btn class
content = content.replace(
    '''class="nav-btn px-3 py-2 rounded-lg text-sm font-medium"''',
    '''class="nav-btn w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-all text-left"'''
)
content = content.replace(
    '''class="nav-btn px-3 py-2 rounded-lg text-sm font-bold border border-scg-200 shadow-sm ml-2"''',
    '''class="nav-btn w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-bold border border-scg-200 shadow-sm transition-all text-left mt-2"'''
)

# Replace all icon margin-right with width-5 text-center
content = content.replace('mr-1"></i>', 'w-5 text-center"></i>')

# Update switchTab logic
old_switch_logic = """            document.querySelectorAll('.nav-btn').forEach(btn => {
                btn.className = btn.id === 'nav-admin' 
                    ? 'nav-btn px-3 py-2 rounded-lg text-sm font-bold text-scg-700 bg-scg-50 border border-scg-200 shadow-sm hover:bg-scg-100 ml-2' 
                    : 'nav-btn px-3 py-2 rounded-lg text-sm font-medium transition-colors text-slate-600 hover:text-scg-800 hover:bg-scg-50';
            });
            
            const activeBtn = document.getElementById(`nav-${tabId}`);
            if(activeBtn) {
                activeBtn.classList.add('bg-scg-800', 'text-white', 'shadow-md');
                activeBtn.classList.remove('text-slate-600', 'hover:bg-scg-50', 'text-scg-700', 'bg-scg-50');
            }"""

new_switch_logic = """            document.querySelectorAll('.nav-btn').forEach(btn => {
                btn.className = btn.id === 'nav-admin' 
                    ? 'nav-btn w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-bold text-scg-700 bg-scg-50 border border-scg-200 shadow-sm hover:bg-scg-100 text-left mt-2 transition-all' 
                    : 'nav-btn w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium text-slate-600 hover:text-scg-800 hover:bg-scg-50 text-left transition-all';
            });
            
            const activeBtn = document.getElementById(`nav-${tabId}`);
            if(activeBtn) {
                activeBtn.classList.add('bg-scg-800', 'text-white', 'shadow-md');
                activeBtn.classList.remove('text-slate-600', 'hover:bg-scg-50', 'text-scg-700', 'bg-scg-50');
            }"""

content = content.replace(old_switch_logic, new_switch_logic)

with open('build_frontend.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated nav logic!")
