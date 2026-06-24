import os
import re

filepaths = [
    'd:/Work/งานใหม่/อบรม/2026/Vibe Coding Workshop/Project/contractor-skill/index_render.html',
    'd:/Work/งานใหม่/อบรม/2026/Vibe Coding Workshop/Project/contractor-skill/static/index.html'
]

mobile_header = """        <!-- MOBILE HEADER -->
        <div class="md:hidden w-full bg-white border-b border-slate-200 flex items-center justify-between p-4 sticky top-0 z-30 shadow-sm shrink-0">
            <div class="flex items-center gap-3">
                <div class="bg-scg-800 text-white p-2 rounded-lg shadow-sm"><i class="fa-solid fa-handshake-angle"></i></div>
                <span class="text-lg font-bold text-scg-900 tracking-tight leading-none">Contractor<br/><span class="text-scg-400"> skill</span></span>
            </div>
            <button onclick="toggleMobileMenu()" class="text-slate-600 hover:text-scg-800 focus:outline-none p-2 bg-slate-50 rounded-lg border border-slate-100">
                <i class="fa-solid fa-bars text-xl"></i>
            </button>
        </div>

        <!-- MOBILE OVERLAY -->
        <div id="mobile-overlay" class="fixed inset-0 bg-slate-900/50 backdrop-blur-sm z-40 hidden md:hidden" onclick="toggleMobileMenu()"></div>

        <!-- SIDEBAR -->
        <aside id="main-sidebar"
            class="fixed md:static inset-y-0 left-0 transform -translate-x-full md:translate-x-0 transition-transform duration-300 ease-in-out w-[280px] md:w-64 bg-white border-r border-slate-200 flex flex-col md:sticky md:top-0 md:h-screen z-50 shadow-2xl md:shadow-sm shrink-0">
            <!-- Close button for mobile -->
            <div class="md:hidden absolute top-4 right-4 z-50">
                <button onclick="toggleMobileMenu()" class="text-slate-400 hover:text-red-500 bg-slate-50 rounded-full p-2 w-8 h-8 flex items-center justify-center border border-slate-100 shadow-sm">
                    <i class="fa-solid fa-xmark"></i>
                </button>
            </div>"""

old_sidebar_start = """        <!-- SIDEBAR -->
        <aside
            class="w-full md:w-64 bg-white border-r border-slate-200 flex flex-col md:sticky md:top-0 md:h-screen z-40 shadow-sm shrink-0">"""

js_toggle_func = """        // Mobile menu toggle
        window.toggleMobileMenu = function() {
            const sidebar = document.getElementById('main-sidebar');
            const overlay = document.getElementById('mobile-overlay');
            if (sidebar.classList.contains('-translate-x-full')) {
                sidebar.classList.remove('-translate-x-full');
                overlay.classList.remove('hidden');
            } else {
                sidebar.classList.add('-translate-x-full');
                overlay.classList.add('hidden');
            }
        };"""

for filepath in filepaths:
    if not os.path.exists(filepath):
        print(f"Skipping {filepath}, not found")
        continue
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Inject Header and replace Sidebar class
    if 'id="main-sidebar"' not in content:
        content = content.replace(old_sidebar_start, mobile_header)

    # 2. Inject JS Toggle function
    if 'window.toggleMobileMenu = function()' not in content:
        if 'function handleLogout() {' in content:
            content = content.replace('function handleLogout() {', js_toggle_func + '\\n\\n        function handleLogout() {')

    # 3. Fix main content padding for mobile
    old_main_class = 'class="flex-grow w-full md:w-[calc(100%-16rem)] md:h-screen overflow-y-auto px-4 sm:px-8 py-8 transition-all duration-300"'
    new_main_class = 'class="flex-grow w-full md:w-[calc(100%-16rem)] md:h-screen overflow-y-auto px-4 sm:px-8 py-4 sm:py-8 transition-all duration-300 relative"'
    content = content.replace(old_main_class, new_main_class)

    # 4. Wrap tables
    # 4.1 Static table 1
    old_static_table = '                        <table class="w-full text-left border-collapse whitespace-nowrap text-sm min-w-max relative"'
    new_static_table = '                        <div class="overflow-x-auto w-full">\\n                            <table class="w-full text-left border-collapse whitespace-nowrap text-sm min-w-max relative"'
    
    if '<div class="overflow-x-auto w-full">' not in content and old_static_table in content:
        # replace starting tags
        content = content.replace(old_static_table, new_static_table)
        
        # replace closing tags (find `</table>` for these specific blocks)
        # Actually, let's use regex to find all <table class="w-full text-left border-collapse whitespace-nowrap text-sm min-w-max relative"...</table>
        # It's safer to just wrap them if they don't have `<div class="overflow-x-auto">` above them.
        
    # We will use Regex to wrap ALL tables that are NOT inside an overflow-x-auto div
    # Wait, simpler logic:
    # Find all occurrences of `<table` and `</table>` that need wrapping in python script.
    
    # 4.2 JS Generated tables
    old_tbl_str = 'let html = `<table class="w-full text-left border-collapse text-sm"><thead><tr class="bg-slate-50 border-b border-slate-100 text-slate-600"><th class="p-4 font-semibold min-w-[200px] w-1/4">Competency</th>`;'
    new_tbl_str = 'let html = `<div class="overflow-x-auto w-full"><table class="w-full text-left border-collapse text-sm"><thead><tr class="bg-slate-50 border-b border-slate-100 text-slate-600"><th class="p-4 font-semibold min-w-[200px] w-1/4">Competency</th>`;'
    if old_tbl_str in content:
        content = content.replace(old_tbl_str, new_tbl_str)
        old_tbl_end = "html += '</tbody></table>';"
        new_tbl_end = "html += '</tbody></table></div>';"
        content = content.replace(old_tbl_end, new_tbl_end)

    old_tbl2_str = "html += '<table class=\"w-full text-left border-collapse min-w-[800px]\">';"
    new_tbl2_str = "html += '<div class=\"overflow-x-auto w-full\"><table class=\"w-full text-left border-collapse min-w-[800px]\">';"
    if old_tbl2_str in content:
        content = content.replace(old_tbl2_str, new_tbl2_str)
        # the end of this table is probably similar
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print(f"Patched {filepath}")
