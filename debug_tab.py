with open('d:/Work/งานใหม่/อบรม/2026/Vibe Coding Workshop/Project/competency-system/index_render.html', 'r', encoding='utf-8') as f:
    html = f.read()

start = html.find('id="tab-training"')
if start != -1:
    end = html.find('</section>', start)
    code = html[start:end]
    print('job-group-filters:', 'job-group-filters' in code)
    print('position-filters:', 'position-filters' in code)
    print('section-filters:', 'section-filters' in code)
    print('employee-filters:', 'employee-filters' in code)
else:
    print('Not found')
