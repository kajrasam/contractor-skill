import re

def reorder_datasets(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # We need to reorder the push statements for activeDatasetsBar and activeDatasets
    # 1. Dashboard (AverageBarChart)
    content = re.sub(
        r"(if \(activeFilters\.includes\('target'\)\) activeDatasetsBar\.push\(\{ label: 'Average Expected'.*?\n)(\s*if \(activeFilters\.includes\('actual'\)\).*?\n)(\s*if \(activeFilters\.includes\('self'\)\).*?\n)(\s*if \(activeFilters\.includes\('before'\)\).*?\n)",
        r"\1\4\3\2",
        content,
        flags=re.DOTALL
    )

    # 2. Individual Dashboard (Radar Chart)
    content = re.sub(
        r"(if \(activeFilters\.includes\('target'\)\) activeDatasets\.push\(\{ label: 'Target'.*?\n)(\s*if \(activeFilters\.includes\('actual'\)\).*?\n)(\s*if \(activeFilters\.includes\('self'\)\).*?\n)(\s*if \(activeFilters\.includes\('before'\)\).*?\n)",
        r"\1\4\3\2",
        content,
        flags=re.DOTALL
    )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Reordered datasets in", filepath)

reorder_datasets('static/index.html')
reorder_datasets('index_render.html')
