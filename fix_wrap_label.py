import os

def patch_file(filepath):
    if not os.path.exists(filepath):
        return
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    target_wrap = """<script>

        const API_BASE = '/api';"""
    
    replacement_wrap = """<script>
        window.wrapLabel = function(text, maxLength = 30) {
            if (text.length <= maxLength) return text;
            const lines = [];
            let currentLine = '';
            const words = text.split(' ');
            for (let w of words) {
                if (w.length > maxLength) {
                    if (currentLine) { lines.push(currentLine.trim()); currentLine = ''; }
                    for (let i = 0; i < w.length; i += maxLength) {
                        lines.push(w.slice(i, i + maxLength));
                    }
                } else if ((currentLine + w).length > maxLength) {
                    if (currentLine) lines.push(currentLine.trim());
                    currentLine = w + ' ';
                } else {
                    currentLine += w + ' ';
                }
            }
            if (currentLine) lines.push(currentLine.trim());
            return lines.length > 1 ? lines : lines[0];
        };

        const API_BASE = '/api';"""

    if target_wrap in html:
        html = html.replace(target_wrap, replacement_wrap)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"Patched {filepath}")
    else:
        print(f"Target not found in {filepath}")

patch_file('index_render.html')
patch_file('static/index.html')
