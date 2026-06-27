import re

def fix_save_eval(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Grab elBefore in saveEvaluation loop
    old_grab_actual = """                // Grab actual eval if exists
                const elActual = document.getElementById(`eval-actual-${id}-${i}`);
                if (elActual) {
                    emp.actuals[i] = parseInt(elActual.value);
                }"""
    
    new_grab_actual = """                // Grab actual eval if exists
                const elActual = document.getElementById(`eval-actual-${id}-${i}`);
                if (elActual) {
                    emp.actuals[i] = parseInt(elActual.value);
                }

                // Grab before eval if exists
                const elBefore = document.getElementById(`eval-before-${id}-${i}`);
                if (elBefore) {
                    if (!emp.before_evals) emp.before_evals = [];
                    emp.before_evals[i] = parseInt(elBefore.value);
                }"""

    content = content.replace(old_grab_actual, new_grab_actual)

    # 2. Add beforeEvals to fetch payload
    old_payload = """                    userId: id,
                    actuals: emp.actuals,
                    selfEvals: emp.self_evals,"""
                    
    new_payload = """                    userId: id,
                    actuals: emp.actuals,
                    selfEvals: emp.self_evals,
                    beforeEvals: emp.before_evals,"""
                    
    content = content.replace(old_payload, new_payload)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Patched {filepath}")

fix_save_eval('static/index.html')
fix_save_eval('index_render.html')
