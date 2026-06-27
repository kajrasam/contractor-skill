with open('static/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "currentUser.id === 'Admin'" in line:
        print(f'{i}: {line.strip()}')
