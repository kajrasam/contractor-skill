import os

def patch_file(filepath):
    if not os.path.exists(filepath):
        return
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Patch Top Performers labels generation to use window.wrapLabel
    target_top_labels = "labels.push(competencies[idx].name.replace(/^[0-9\\.\\s]+/, ''));"
    replacement_top_labels = "labels.push(window.wrapLabel(competencies[idx].name.replace(/^[0-9\\.\\s]+/, ''), 30));"

    if target_top_labels in html:
        html = html.replace(target_top_labels, replacement_top_labels)
        print(f"Patched Top Performers labels in {filepath}")
    else:
        print(f"Top Performers labels target not found in {filepath}")

    # 2. Patch Top Performers chart options to add padding
    target_top_options = """options: {
                            responsive: true,
                            maintainAspectRatio: false,
                            plugins: {"""
    replacement_top_options = """options: {
                            responsive: true,
                            maintainAspectRatio: false,
                            layout: { padding: 15 },
                            plugins: {"""
    
    if target_top_options in html:
        html = html.replace(target_top_options, replacement_top_options)
        print(f"Patched Top Performers options in {filepath}")
    else:
        print(f"Top Performers options target not found in {filepath}")

    # 3. Patch IDP chart options to add padding
    target_idp_options = """options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {"""
    replacement_idp_options = """options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    layout: { padding: 15 },
                    plugins: {"""
    
    if target_idp_options in html:
        html = html.replace(target_idp_options, replacement_idp_options)
        print(f"Patched IDP options in {filepath}")
    else:
        print(f"IDP options target not found in {filepath}")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Finished patching {filepath}")

patch_file('index_render.html')
patch_file('static/index.html')
