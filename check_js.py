from bs4 import BeautifulSoup
import subprocess

with open('d:/Work/งานใหม่/อบรม/2026/Vibe Coding Workshop/Project/competency-system/static/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')
scripts = soup.find_all('script')

for i, script in enumerate(scripts):
    if script.string:
        with open(f'temp_script_{i}.js', 'w', encoding='utf-8') as sf:
            sf.write(script.string)
        
        try:
            subprocess.run(['node', '-c', f'temp_script_{i}.js'], check=True, capture_output=True, text=True)
            print(f'Script {i} is OK')
        except subprocess.CalledProcessError as e:
            print(f'Script {i} Error:', e.stderr)
