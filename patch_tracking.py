import re

def fix_tracking_table(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update th tags
    th_old = r'<th class="py-4 px-6 border-r border-slate-100 text-center">ประเมินตนเอง</th>\s*<th class="py-4 px-6 text-center">ผู้บังคับบัญชาประเมิน</th>'
    th_new = r'''<th class="py-4 px-6 border-r border-slate-100 text-center">ประเมินตนเอง</th>
                                <th class="py-4 px-6 border-r border-slate-100 text-center">ประเมิน(Before)</th>
                                <th class="py-4 px-6 text-center">ประเมิน(After)</th>'''
    content = re.sub(th_old, th_new, content)

    # 2. Update selfDate and mgrDate block
    js_logic_old = r'''let selfDate = '';
        let mgrDate = '';
        if \(u\) \{
            if \(u\.evalDate && u\.evalDate\.startsWith\('\{'\)\) \{'''
            
    js_logic_new = r'''let selfDate = '';
        let mgrDate = '';
        let hasBefore = false;
        let hasAfter = false;
        if (u) {
            if (u.before_evals && u.before_evals.some(v => v > 0)) hasBefore = true;
            if (u.actuals && u.actuals.some(v => v > 0)) hasAfter = true;
            if (u.evalDate && u.evalDate.startsWith('{')) {'''
    content = re.sub(js_logic_old, js_logic_new, content)

    # 3. Update trackingList.push
    push_old = r'''selfDate: selfDate,\s*mgrDate: mgrDate\s*\}\);'''
    push_new = r'''selfDate: selfDate,
                    mgrDate: mgrDate,
                    hasBefore: hasBefore,
                    hasAfter: hasAfter
                });'''
    content = re.sub(push_old, push_new, content)

    # 4. Update html +=
    td_old = r'''<td class="py-3 px-6 border-r border-slate-100 text-center text-xs text-slate-600">\$\{t\.selfDate \|\| ''\}</td>\s*<td class="py-3 px-6 text-center text-xs text-slate-600">\$\{t\.mgrDate \|\| ''\}</td>'''
    td_new = r'''<td class="py-3 px-6 border-r border-slate-100 text-center text-xs text-slate-600">${t.selfDate || ''}</td>
                                    <td class="py-3 px-6 border-r border-slate-100 text-center text-xs text-slate-600">${(t.hasBefore && t.mgrDate) ? t.mgrDate : ''}</td>
                                    <td class="py-3 px-6 text-center text-xs text-slate-600">${(t.hasAfter && t.mgrDate) ? t.mgrDate : ''}</td>'''
    content = re.sub(td_old, td_new, content)
    
    # 5. colspan="8" to "9"
    colspan_old = r'<td colspan="8"'
    colspan_new = r'<td colspan="9"'
    content = re.sub(colspan_old, colspan_new, content)

    # 6. Update exportTrackingData headers
    header_old = r'"ประเมินตนเอง", "ผู้บังคับบัญชาประเมิน"'
    header_new = r'"ประเมินตนเอง", "ประเมิน(Before)", "ประเมิน(After)"'
    content = re.sub(header_old, header_new, content)

    # 7. Update export logic cols
    export_cols_old = r'''if \(cols\.length >= 8\) \{\s*const rowData = \[\s*cols\[1\]\.innerText\.trim\(\),\s*cols\[2\]\.innerText\.trim\(\),\s*cols\[3\]\.innerText\.trim\(\),\s*cols\[4\]\.querySelector\('i'\) \? 'Yes' : '',\s*cols\[5\]\.querySelector\('i'\) \? 'Yes' : '',\s*cols\[6\]\.innerText\.trim\(\),\s*cols\[7\]\.innerText\.trim\(\)\s*\]\.map\(val => `"\$\{val\.replace\(/"/g, '""'\)\}"`\);'''
    export_cols_new = r'''if (cols.length >= 9) {
                const rowData = [
                    cols[1].innerText.trim(),
                    cols[2].innerText.trim(),
                    cols[3].innerText.trim(),
                    cols[4].querySelector('i') ? 'Yes' : '',
                    cols[5].querySelector('i') ? 'Yes' : '',
                    cols[6].innerText.trim(),
                    cols[7].innerText.trim(),
                    cols[8].innerText.trim()
                ].map(val => `"${val.replace(/"/g, '""')}"`);'''
    content = re.sub(export_cols_old, export_cols_new, content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Patched {filepath}")

fix_tracking_table('static/index.html')
fix_tracking_table('index_render.html')
