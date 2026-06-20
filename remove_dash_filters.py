import re

files = [
    'd:/Work/งานใหม่/อบรม/2026/Vibe Coding Workshop/Project/competency-system/static/index.html',
    'd:/Work/งานใหม่/อบรม/2026/Vibe Coding Workshop/Project/competency-system/index_render.html'
]

for file_path in files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Remove HTML
    html_pattern = re.compile(
        r'<!-- Filters -->.*?<!-- Manager Chart: Average Clustered Column -->',
        re.DOTALL
    )
    content = html_pattern.sub('<!-- Manager Chart: Average Clustered Column -->', content)

    # Clean up the container if needed (from flex to block)
    content = content.replace(
        '<div class="mb-6 flex flex-col md:flex-row justify-between items-start md:items-end gap-4">\n                    <div>',
        '<div class="mb-6">\n                    <div>'
    )

    # 2. Remove let selectedDashJobGroupFilter = [];
    content = content.replace('let selectedDashJobGroupFilter = [];\n', '')
    content = content.replace('        let selectedDashPosFilter = [];\n', '')

    # 3. Remove buildDashFiltersUI() call
    content = content.replace('            buildDashFiltersUI();\n', '')

    # 4. Remove Apply Filters logic
    js_filters_pattern = re.compile(
        r'// Apply Filters.*?if\(selectedDashPosFilter\.length > 0\) \{[^\}]+?\}\s*\}',
        re.DOTALL
    )
    content = js_filters_pattern.sub('', content)

    # 5. Remove functions buildDashFiltersUI and toggleDashFilter
    functions_pattern = re.compile(
        r'function buildDashFiltersUI\(\).*?window\.toggleDashFilter\s*=\s*function\(type,\s*value\)\s*\{.*?\};',
        re.DOTALL
    )
    content = functions_pattern.sub('', content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

print("Patch applied.")
