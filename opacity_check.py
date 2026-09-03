with open('app/static/css/style.css', 'r') as f:
    lines = f.readlines()
    
for i, line in enumerate(lines, 1):
    if 'opacity' in line.lower():
        print(f"Line {i}: {line.rstrip()}")