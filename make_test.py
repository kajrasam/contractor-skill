import re
with open('static/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

logger = '''<script>
window.errors = [];
window.onerror = function(message, source, lineno, colno, error) {
    alert("Error: " + message + " at line " + lineno);
};
</script>'''
html = html.replace('<head>', '<head>' + logger)
with open('test_error.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('test_error.html created')
