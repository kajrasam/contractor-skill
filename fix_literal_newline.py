import re

def fix_newline(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # The buggy string literal spans two lines:
    # let csvContent = "\uFEFF" + "Employee Name,Position name,Average Expected,Average Before,Average Self Eva,Average Actual,% Complete
    # ";
    
    old_str = 'let csvContent = "\\uFEFF" + "Employee Name,Position name,Average Expected,Average Before,Average Self Eva,Average Actual,% Complete\n";'
    new_str = 'let csvContent = "\\uFEFF" + "Employee Name,Position name,Average Expected,Average Before,Average Self Eva,Average Actual,% Complete\\n";'
    
    content = content.replace(old_str, new_str)
    
    # Also check the second one:
    # csvContent += `"${empName}","${position}",${avgT},${avgB},${avgS},${avgA},${percent}%
    # `;
    
    # Wait, backticks DO support multiline! So the second one is technically valid JS, 
    # but it would insert actual newlines in the CSV which is fine because CSV rows are separated by newlines!
    # BUT let's change it to \n anyway just to be safe and clean.
    old_str2 = 'csvContent += `"${empName}","${position}",${avgT},${avgB},${avgS},${avgA},${percent}%\n`;'
    new_str2 = 'csvContent += `"${empName}","${position}",${avgT},${avgB},${avgS},${avgA},${percent}%\\n`;'
    content = content.replace(old_str2, new_str2)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Fixed {filepath}")

fix_newline('static/index.html')
fix_newline('index_render.html')
