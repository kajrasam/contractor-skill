import re

def fix_employee_data_filter(fp):
    with open(fp, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace the filtering logic
    new_content = content.replace("employeeData = employeeDataAll.filter(e => e.Pipeline === 'Evaluated');", "employeeData = [...employeeDataAll];")
    
    # Let's also check if there is any other place where e.Pipeline === 'Evaluated' is used
    new_content = new_content.replace("is_evaluated: e.Pipeline === 'Evaluated',", "is_evaluated: true,")
    
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(new_content)
        
for fp in ['index_render.html', 'static/index.html']:
    fix_employee_data_filter(fp)

print("Fixed employeeData filter")
