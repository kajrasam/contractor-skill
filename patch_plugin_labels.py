import re

def patch_plugin(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Look for the plugin block
    old_plugin = """                                } else if (dataset.label === 'Average Actual' && value > 0) {
                                    ctx.fillStyle = '#9f1239';
                                    ctx.font = 'bold 11px sans-serif';
                                    ctx.textAlign = 'center';
                                    ctx.textBaseline = 'bottom';
                                    ctx.fillText(value, datapoint.x, datapoint.y - 5);
                                }"""
                                
    new_plugin = """                                } else if (dataset.label === 'Average Actual' && value > 0) {
                                    ctx.fillStyle = '#9f1239';
                                    ctx.font = 'bold 11px sans-serif';
                                    ctx.textAlign = 'center';
                                    ctx.textBaseline = 'bottom';
                                    ctx.fillText(value, datapoint.x, datapoint.y - 5);
                                } else if (dataset.label === 'Average Before' && value > 0) {
                                    ctx.fillStyle = '#7e22ce';
                                    ctx.font = 'bold 11px sans-serif';
                                    ctx.textAlign = 'center';
                                    ctx.textBaseline = 'bottom';
                                    ctx.fillText(value, datapoint.x, datapoint.y - 5);
                                } else if (dataset.label === 'Average Self' && value > 0) {
                                    ctx.fillStyle = '#b45309';
                                    ctx.font = 'bold 11px sans-serif';
                                    ctx.textAlign = 'center';
                                    ctx.textBaseline = 'bottom';
                                    ctx.fillText(value, datapoint.x, datapoint.y - 5);
                                }"""

    content = content.replace(old_plugin, new_plugin)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Patched plugin in {filepath}")

patch_plugin('static/index.html')
patch_plugin('index_render.html')
