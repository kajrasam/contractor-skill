import re

def swap_formats(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Update Self Eva. to purple dotted
    # Find: { label: 'Self Eva.', ... borderColor: '#fbbf24', backgroundColor: 'rgba(251, 191, 36, 0.2)' ... }
    # Since there are variations in borderWidth and points, we just replace the base colors and add borderDash.
    
    # Let's be precise.
    # Replace Self Eva base color and add border dash
    content = re.sub(
        r"label:\s*'Self Eva\.',\s*data:\s*([^,]+),\s*borderColor:\s*'#fbbf24',\s*backgroundColor:\s*'rgba\(251, 191, 36, 0.2\)'",
        r"label: 'Self Eva.', data: \1, borderColor: '#9333ea', backgroundColor: 'transparent', borderDash: [5, 5]",
        content
    )
    # Also replace any point colors for Self Eva if they exist (fbbf24 to 9333ea)
    # Actually it's easier to do this in two passes or carefully.
    
    # Let's restore the full string replacement strategy by reading lines and replacing known strings
    # We have exact strings from grep:
    
    replacements = {
        # --- Base Radar ---
        "label: 'Self Eva.', data: selfEvals, borderColor: '#fbbf24', backgroundColor: 'rgba(251, 191, 36, 0.2)'": "label: 'Self Eva.', data: selfEvals, borderColor: '#9333ea', backgroundColor: 'transparent', borderDash: [5, 5]",
        
        "label: 'Before', data: beforeEvals, borderColor: '#9333ea', backgroundColor: 'transparent', borderDash: [2, 2]": "label: 'Before', data: beforeEvals, borderColor: '#fbbf24', backgroundColor: 'rgba(251, 191, 36, 0.2)'",
        
        # --- Filtered Radar ---
        "label: 'Self Eva.', data: cleanSelfs, borderColor: '#fbbf24', backgroundColor: 'rgba(251, 191, 36, 0.2)'": "label: 'Self Eva.', data: cleanSelfs, borderColor: '#9333ea', backgroundColor: 'transparent', borderDash: [5, 5]",
        
        "label: 'Before', data: cleanBefores, borderColor: '#9333ea', backgroundColor: 'transparent', borderDash: [2, 2]": "label: 'Before', data: cleanBefores, borderColor: '#fbbf24', backgroundColor: 'rgba(251, 191, 36, 0.2)'",
        
        # --- IDP Radar ---
        "label: 'Self Eva.', data: selfEvals, borderColor: '#fbbf24', backgroundColor: 'rgba(251, 191, 36, 0.2)', borderWidth: 2, pointBackgroundColor: '#fbbf24', pointBorderColor: '#fff', pointHoverBackgroundColor: '#fff', pointHoverBorderColor: '#fbbf24', pointRadius: 4": "label: 'Self Eva.', data: selfEvals, borderColor: '#9333ea', backgroundColor: 'transparent', borderDash: [5, 5], borderWidth: 2, pointBackgroundColor: '#9333ea', pointBorderColor: '#fff', pointHoverBackgroundColor: '#fff', pointHoverBorderColor: '#9333ea', pointRadius: 4",
        
        "label: 'Before', data: window.beforeEvalsLocal, borderColor: '#9333ea', backgroundColor: 'transparent', borderDash: [2, 2], borderWidth: 2, pointBackgroundColor: '#9333ea', pointBorderColor: '#fff', pointHoverBackgroundColor: '#fff', pointHoverBorderColor: '#9333ea', pointRadius: 4": "label: 'Before', data: window.beforeEvalsLocal, borderColor: '#fbbf24', backgroundColor: 'rgba(251, 191, 36, 0.2)', borderWidth: 2, pointBackgroundColor: '#fbbf24', pointBorderColor: '#fff', pointHoverBackgroundColor: '#fff', pointHoverBorderColor: '#fbbf24', pointRadius: 4",
        
        # --- Analytic Radar ---
        "label: 'Self Eva.', data: selfData, borderColor: '#fbbf24', backgroundColor: 'rgba(251, 191, 36, 0.2)', borderWidth: 2, pointBackgroundColor: '#fbbf24', pointBorderColor: '#fff', pointHoverBackgroundColor: '#fff', pointHoverBorderColor: '#fbbf24', pointRadius: 3": "label: 'Self Eva.', data: selfData, borderColor: '#9333ea', backgroundColor: 'transparent', borderDash: [5, 5], borderWidth: 2, pointBackgroundColor: '#9333ea', pointBorderColor: '#fff', pointHoverBackgroundColor: '#fff', pointHoverBorderColor: '#9333ea', pointRadius: 3",
        
        "label: 'Before', data: beforeData, borderColor: '#9333ea', backgroundColor: 'transparent', borderDash: [2, 2], borderWidth: 2, pointBackgroundColor: '#9333ea', pointBorderColor: '#fff', pointHoverBackgroundColor: '#fff', pointHoverBorderColor: '#9333ea', pointRadius: 3": "label: 'Before', data: beforeData, borderColor: '#fbbf24', backgroundColor: 'rgba(251, 191, 36, 0.2)', borderWidth: 2, pointBackgroundColor: '#fbbf24', pointBorderColor: '#fff', pointHoverBackgroundColor: '#fff', pointHoverBorderColor: '#fbbf24', pointRadius: 3"
    }

    for old_str, new_str in replacements.items():
        if old_str in content:
            content = content.replace(old_str, new_str)
        else:
            print(f"Warning: String not found in {filepath}: {old_str[:50]}...")
            
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Patched {filepath}")

import os
if os.path.exists('static/index.html'): swap_formats('static/index.html')
if os.path.exists('index_render.html'): swap_formats('index_render.html')
