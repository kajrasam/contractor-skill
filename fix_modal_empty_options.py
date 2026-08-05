import sys

for fp in ['index_render.html', 'static/index.html']:
    with open(fp, 'r', encoding='utf-8') as f:
        c = f.read()

    # Modify getUniqueValues to support multiple fields via comma-separated string
    old_guv = '''function getUniqueValues(data, field) {
            const vals = data.map(d => d[field]).filter(v => v);
            return [...new Set(vals)].sort();
        }'''
    
    new_guv = '''function getUniqueValues(data, field) {
            const fields = field.split(',');
            const vals = data.map(d => {
                for(let f of fields) {
                    if(d[f.trim()]) return d[f.trim()];
                }
                return null;
            }).filter(v => v);
            return [...new Set(vals)].sort();
        }'''
    
    c = c.replace(old_guv, new_guv)
    
    # Replace the calls to getUniqueValues with comma separated fallbacks
    c = c.replace("'CompanyThai'", "'CompanyThai, company'")
    c = c.replace("'Sub1CompanyThai'", "'Sub1CompanyThai, sub1_company'")
    c = c.replace("'DivisionThai'", "'DivisionThai, division'")
    c = c.replace("'Sub1DivisionThai'", "'Sub1DivisionThai, sub1_division'")
    c = c.replace("'DepartmentThai'", "'DepartmentThai, department'")
    c = c.replace("'SectionThai'", "'SectionThai, section'")
    c = c.replace("'PositionNameThai'", "'PositionNameThai, position_name'")
    c = c.replace("'PositionStructureLevel'", "'PositionStructureLevel, position_level'")
    c = c.replace("'JobGroup'", "'JobGroup, job_group'")

    # Extra fallback logic inside the filter conditionals!
    c = c.replace("e.CompanyThai ===", "(e.CompanyThai || e.company) ===")
    c = c.replace("e.Sub1CompanyThai ===", "(e.Sub1CompanyThai || e.sub1_company) ===")
    c = c.replace("e.DivisionThai ===", "(e.DivisionThai || e.division) ===")
    c = c.replace("e.Sub1DivisionThai ===", "(e.Sub1DivisionThai || e.sub1_division) ===")
    c = c.replace("e.DepartmentThai ===", "(e.DepartmentThai || e.department) ===")
    c = c.replace("e.SectionThai ===", "(e.SectionThai || e.section) ===")
    c = c.replace("e.PositionNameThai ===", "(e.PositionNameThai || e.position_name) ===")

    with open(fp, 'w', encoding='utf-8') as f:
        f.write(c)
