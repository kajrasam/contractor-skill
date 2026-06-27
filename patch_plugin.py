import re

def patch_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    old_plugin = """                plugins: [{
                    id: 'customDataLabels',
                    afterDatasetsDraw(chart, args, pluginOptions) {
                        const { ctx, data } = chart;
                        ctx.save();

                        // Dataset 0 is the % Complete line
                        chart.getDatasetMeta(0).data.forEach((datapoint, index) => {
                            const value = data.datasets[0].data[index] + '%';
                            ctx.fillStyle = '#b45309';
                            ctx.font = 'bold 12px sans-serif';
                            ctx.textAlign = 'center';
                            ctx.textBaseline = 'bottom';
                            ctx.fillText(value, datapoint.x, datapoint.y - 10);
                        });

                        // Dataset 1 is the Average Expected
                        chart.getDatasetMeta(1).data.forEach((datapoint, index) => {
                            const value = data.datasets[1].data[index];
                            if (value > 0) {
                                ctx.fillStyle = '#64748b'; // slate-500
                                ctx.font = 'bold 11px sans-serif';
                                ctx.textAlign = 'center';
                                ctx.textBaseline = 'bottom';
                                ctx.fillText(value, datapoint.x, datapoint.y - 5);
                            }
                        });

                        // Dataset 2 is the Average Actual
                        chart.getDatasetMeta(2).data.forEach((datapoint, index) => {
                            const value = data.datasets[2].data[index];
                            if (value > 0) {
                                ctx.fillStyle = '#9f1239'; // rose-900
                                ctx.font = 'bold 11px sans-serif';
                                ctx.textAlign = 'center';
                                ctx.textBaseline = 'bottom';
                                ctx.fillText(value, datapoint.x, datapoint.y - 5);
                            }
                        });

                        ctx.restore();
                    }
                }]"""
    
    new_plugin = """                plugins: [{
                    id: 'customDataLabels',
                    afterDatasetsDraw(chart, args, pluginOptions) {
                        const { ctx, data } = chart;
                        ctx.save();

                        data.datasets.forEach((dataset, i) => {
                            const meta = chart.getDatasetMeta(i);
                            if (!meta || meta.hidden) return;
                            
                            meta.data.forEach((datapoint, index) => {
                                const value = dataset.data[index];
                                if (value === undefined || value === null) return;
                                
                                if (dataset.label === '% Complete') {
                                    ctx.fillStyle = '#b45309';
                                    ctx.font = 'bold 12px sans-serif';
                                    ctx.textAlign = 'center';
                                    ctx.textBaseline = 'bottom';
                                    ctx.fillText(value + '%', datapoint.x, datapoint.y - 10);
                                } else if (dataset.label === 'Average Expected' && value > 0) {
                                    ctx.fillStyle = '#64748b';
                                    ctx.font = 'bold 11px sans-serif';
                                    ctx.textAlign = 'center';
                                    ctx.textBaseline = 'bottom';
                                    ctx.fillText(value, datapoint.x, datapoint.y - 5);
                                } else if (dataset.label === 'Average Actual' && value > 0) {
                                    ctx.fillStyle = '#9f1239';
                                    ctx.font = 'bold 11px sans-serif';
                                    ctx.textAlign = 'center';
                                    ctx.textBaseline = 'bottom';
                                    ctx.fillText(value, datapoint.x, datapoint.y - 5);
                                }
                            });
                        });

                        ctx.restore();
                    }
                }]"""
    html = html.replace(old_plugin, new_plugin)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Patched plugin in {filepath}")

patch_file('static/index.html')
patch_file('index_render.html')
