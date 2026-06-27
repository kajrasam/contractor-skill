import os
import re

def fix_app():
    with open('app.py', 'r', encoding='utf-8') as f:
        content = f.read()

    # Part 1: get_data parsing
    # Default values
    content = content.replace('scope_sec = ""\n            scope_dep = ""\n', 'scope_sec = ""\n            scope_dep = ""\n            scope_div = []\n')
    
    # JSON parsing
    content = content.replace('scope_sec = parsed.get("scope_section", "")\n                    scope_dep = parsed.get("scope_department", "")\n', 'scope_sec = parsed.get("scope_section", "")\n                    scope_dep = parsed.get("scope_department", "")\n                    scope_div = parsed.get("scope_division", [])\n')
    
    # JSON parsing assignment
    content = content.replace('"scope_section": scope_sec,\n                "scope_department": scope_dep,\n', '"scope_section": scope_sec,\n                "scope_department": scope_dep,\n                "scope_division": scope_div,\n')

    # Part 2: POST /api/admin_users
    content = content.replace('scope_sec = data.get(\'scope_section\', \'\')\n    scope_dep = data.get(\'scope_department\', \'\')\n', 'scope_sec = data.get(\'scope_section\', \'\')\n    scope_dep = data.get(\'scope_department\', \'\')\n    scope_div = data.get(\'scope_division\', [])\n')
    
    content = content.replace('detail = json.dumps({"scope_section": scope_sec, "scope_department": scope_dep})', 'detail = json.dumps({"scope_section": scope_sec, "scope_department": scope_dep, "scope_division": scope_div})')
    
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(content)
        
fix_app()
