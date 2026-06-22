import re

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    # Find matchesFiltersExcept so we don't remove it from there
    idx = html.find('function matchesFiltersExcept(')
    end_matches = html.find('}', html.find('return true;', idx))
    
    # We want to replace the bad injection outside of this function
    bad_string = "            if (ignoreFilter !== 'competency' && !hasCompetencyFilterMatch(posName)) return false;\n"
    
    # Split the html into before, inside, and after matchesFiltersExcept
    before = html[:idx]
    inside = html[idx:end_matches]
    after = html[end_matches:]
    
    # Remove bad string from before and after
    before = before.replace(bad_string, "")
    after = after.replace(bad_string, "")
    
    # Also, we injected with a missing newline or weird indentation in some cases?
    # Let's just do a regex replace to be safe
    bad_regex = r"(\s*)if \(ignoreFilter !== 'competency' && !hasCompetencyFilterMatch\(posName\)\) return false;"
    before = re.sub(bad_regex, "", before)
    after = re.sub(bad_regex, "", after)

    new_html = before + inside + after

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_html)
    print(f"Fixed {filepath}")

fix_file('static/index.html')
fix_file('index_render.html')
