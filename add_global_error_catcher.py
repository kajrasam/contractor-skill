import re

def patch_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    error_catcher = """
    <!-- Global Error Catcher -->
    <script>
        window.addEventListener('error', function(e) {
            const errDiv = document.createElement('div');
            errDiv.style.position = 'fixed';
            errDiv.style.top = '10px';
            errDiv.style.left = '10px';
            errDiv.style.zIndex = '999999';
            errDiv.style.backgroundColor = 'red';
            errDiv.style.color = 'white';
            errDiv.style.padding = '15px';
            errDiv.style.borderRadius = '5px';
            errDiv.style.maxWidth = '90vw';
            errDiv.style.wordWrap = 'break-word';
            errDiv.innerHTML = '<b>JS Error:</b> ' + e.message + '<br><small>File: ' + e.filename + ' Line: ' + e.lineno + '</small><br><pre style="font-size:10px; margin-top:5px; max-height:200px; overflow-y:auto;">' + (e.error && e.error.stack ? e.error.stack : '') + '</pre>';
            document.body.appendChild(errDiv);
        });
        window.addEventListener('unhandledrejection', function(e) {
            const errDiv = document.createElement('div');
            errDiv.style.position = 'fixed';
            errDiv.style.top = '120px';
            errDiv.style.left = '10px';
            errDiv.style.zIndex = '999999';
            errDiv.style.backgroundColor = 'darkred';
            errDiv.style.color = 'white';
            errDiv.style.padding = '15px';
            errDiv.style.borderRadius = '5px';
            errDiv.style.maxWidth = '90vw';
            errDiv.style.wordWrap = 'break-word';
            errDiv.innerHTML = '<b>Promise Error:</b> ' + e.reason;
            document.body.appendChild(errDiv);
        });
    </script>
    """
    
    html = html.replace('</head>', error_catcher + '\n</head>')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Patched global error catcher in {filepath}")

patch_file('static/index.html')
patch_file('index_render.html')
