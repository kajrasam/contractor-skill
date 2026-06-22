import subprocess

with open('d:/Work/งานใหม่/อบรม/2026/Vibe Coding Workshop/Project/competency-system/static/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

parts = html.split('<script>')
for i in range(1, len(parts)):
    script_content = parts[i].split('</script>')[0]
    
    with open(f'temp_script_{i}.js', 'w', encoding='utf-8') as sf:
        sf.write(script_content)
    
    try:
        subprocess.run(['node', '-c', f'temp_script_{i}.js'], check=True, capture_output=True, text=True)
        print(f'Script {i} is OK')
    except subprocess.CalledProcessError as e:
        print(f'Script {i} Error:', e.stderr)
