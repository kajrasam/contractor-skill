import os
import re

def patch_file(filepath):
    if not os.path.exists(filepath):
        return
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Add window.wrapLabel function
    target_wrap = """<script>
        const API_BASE = 'https://competency-system.onrender.com/api';"""
    
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
        const API_BASE = 'https://competency-system.onrender.com/api';"""

    if target_wrap in html:
        html = html.replace(target_wrap, replacement_wrap)
    
    # 2. Patch allLabels generation
    target_allLabels = """const allLabels = getLabels().map(l => {
                const parts = l.split('. ');
                return parts.length > 1 ? parts.slice(1).join('. ') : l;
            });"""
    replacement_allLabels = """const allLabels = getLabels().map(l => {
                const parts = l.split('. ');
                let cleanText = parts.length > 1 ? parts.slice(1).join('. ') : l;
                return window.wrapLabel(cleanText, 30);
            });"""
    html = html.replace(target_allLabels, replacement_allLabels)

    # 3. Patch cleanLabels.push in loops
    target_cleanLabels = """const parts = currentLabels[i].split('. ');
                        cleanLabels.push(parts.length > 1 ? parts.slice(1).join('. ') : currentLabels[i]);"""
    replacement_cleanLabels = """const parts = currentLabels[i].split('. ');
                        let cleanText = parts.length > 1 ? parts.slice(1).join('. ') : currentLabels[i];
                        cleanLabels.push(window.wrapLabel(cleanText, 30));"""
    html = html.replace(target_cleanLabels, replacement_cleanLabels)

    # 4. Patch Chart options for radar charts to include layout padding and smaller font
    # Look for exact current radar options and replace
    target_options1 = """options: { responsive: true, maintainAspectRatio: false, scales: { r: { min: 0, max: 5, ticks: { display: false } } } }"""
    replacement_options1 = """options: { responsive: true, maintainAspectRatio: false, layout: { padding: 15 }, scales: { r: { min: 0, max: 5, ticks: { display: false }, pointLabels: { font: { size: 10 } } } } }"""
    html = html.replace(target_options1, replacement_options1)

    target_options2 = """options: { responsive: true, maintainAspectRatio: false, scales: { r: { min: 0, max: 5, ticks: { display: false } } } }"""
    # replacing again just in case there are multiple, wait replace does all occurrences in string
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Patched {filepath}")

patch_file('index_render.html')
patch_file('static/index.html')
