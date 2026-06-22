import re

def patch_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Fix renderActiveTab to properly rebuild Role&Response and Evaluation tabs
    old_code = """function renderActiveTab() {
            const activeTab = document.querySelector('.tab-content.active');
            if(!activeTab) return;
            const id = activeTab.id.replace('tab-', '');
            if(id === 'training') buildTrainingMatrix();
            if(id === 'dashboard') setupDashboardTab();
            if(id === 'idp') renderIDPContent();
            if(id === 'analytic') renderAnalyticTab();
            if(id === 'admin') renderAdminTable();
        }"""
        
    new_code = """function renderActiveTab() {
            const activeTab = document.querySelector('.tab-content.active');
            if(!activeTab) return;
            const id = activeTab.id.replace('tab-', '');
            if(id === 'training') {
                buildRoleResponseSection();
                buildTrainingMatrix();
            }
            if(id === 'evaluation') setupEvaluationTab();
            if(id === 'dashboard') setupDashboardTab();
            if(id === 'idp') renderIDPContent();
            if(id === 'analytic') renderAnalyticTab();
            if(id === 'admin') renderAdminTable();
        }"""
        
    html = html.replace(old_code, new_code)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Patched {filepath}")

patch_file('static/index.html')
patch_file('index_render.html')
