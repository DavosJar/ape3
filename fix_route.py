#!/usr/bin/env python3
with open('app.py', 'r') as f:
    content = f.read()

# Fix: change /diagramas/ to /diagramas/
old = "@app.route('/diagramas/')\ndef serve_diagram(filename):\n    return send_from_directory('diagrams', filename)"
new = "@app.route('/diagramas/')\ndef serve_diagram(filename):\n    return send_from_directory('diagrams', filename)"

if old in content:
    content = content.replace(old, new)
    with open('app.py', 'w') as f:
        f.write(content)
    print("SUCCESS: Fixed route from '/diagramas/' to '/diagramas/'")
else:
    print("ERROR: Old pattern not found")
    # Find and show current
    import re
    m = re.search(r"@app\.route\(['\"])(.*?)\1.*?def serve_diagram", content, re.DOTALL)
    if m:
        print(f"Current: {m.group(2)}")