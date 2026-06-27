import re

def patch_chart(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update activeDatasetsBar for % Complete
    old_dataset = """let activeDatasetsBar = [
                {
                    type: 'line',
                    label: '% Complete',
                    data: percentCompletes,
                    borderColor: '#eab308',
                    backgroundColor: '#eab308',
                    borderWidth: 2,
                    pointRadius: 6,
                    pointHoverRadius: 8,
                    showLine: false,
                    yAxisID: 'y1'
                }
            ];"""
    
    new_dataset = """let activeDatasetsBar = [
                {
                    type: 'line',
                    label: '% Complete',
                    data: percentCompletes,
                    borderColor: '#16a34a',
                    backgroundColor: '#16a34a',
                    borderWidth: 2,
                    pointRadius: 4.2,
                    pointHoverRadius: 5.6,
                    showLine: false,
                    yAxisID: 'y1'
                }
            ];"""
            
    content = content.replace(old_dataset, new_dataset)

    # 2. Update the text label color for % Complete to match
    old_text_draw = """                    if (dataset.label === '% Complete') {
                        ctx.fillStyle = '#b45309';
                        ctx.font = 'bold 12px sans-serif';
                        ctx.textAlign = 'center';
                        ctx.textBaseline = 'bottom';
                        ctx.fillText(value + '%', datapoint.x, datapoint.y - 10);
                    }"""
                    
    new_text_draw = """                    if (dataset.label === '% Complete') {
                        ctx.fillStyle = '#16a34a';
                        ctx.font = 'bold 12px sans-serif';
                        ctx.textAlign = 'center';
                        ctx.textBaseline = 'bottom';
                        ctx.fillText(value + '%', datapoint.x, datapoint.y - 8);
                    }"""
                    
    content = content.replace(old_text_draw, new_text_draw)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Patched {filepath}")

patch_chart('static/index.html')
patch_chart('index_render.html')
