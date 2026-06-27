import os

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    start_str = '    <script src=\"https://cdn.tailwindcss.com\">\n'
    if start_str in content:
        start_idx = content.find(start_str) + len(start_str)
        # Check if the next line is the function
        if '        function openManageAdminsModal() {' in content[start_idx:start_idx+100]:
            # This is the broken one
            end_idx = content.find('async function deleteAdminUser(uid) {')
            # find the end of deleteAdminUser
            end_idx = content.find('        }', content.find('console.error(e);', end_idx)) + 9
            
            js_block = content[start_idx:end_idx]
            
            # Remove it from the top
            content = content.replace(js_block, '')
            
            # Fix the tailwind script tag
            content = content.replace('<script src=\"https://cdn.tailwindcss.com\">\n\n</script>', '<script src=\"https://cdn.tailwindcss.com\"></script>')
            content = content.replace('<script src=\"https://cdn.tailwindcss.com\">\n\n\n</script>', '<script src=\"https://cdn.tailwindcss.com\"></script>')
            
            # Insert at the bottom
            target = '</body>'
            new_script = '    <script>\n' + js_block + '\n    </script>\n</body>'
            content = content.replace('</body>', new_script)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f'Fixed {filepath}')
        else:
            print(f'Already fixed {filepath}?')

fix_file('index_render.html')
fix_file('static/index.html')
