with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

target = 'from fastapi.responses import FileResponse, HTMLResponse'
replacement = 'from fastapi.responses import FileResponse, HTMLResponse, Response'

if target in content and 'def favicon' not in content:
    content = content.replace(target, replacement, 1)
    
    route_target = '@app.get("/")'
    route_replacement = '''@app.get("/favicon.ico", include_in_schema=False)
def favicon() -> Response:
    svg = \'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><circle cx="16" cy="16" r="15" fill="#101c28"/><path d="M16 3l3 13-3 13-3-13z" fill="#d6ae66"/><circle cx="16" cy="16" r="3" fill="#ece6d6"/></svg>\'
    return Response(content=svg, media_type="image/svg+xml")

@app.get("/")'''
    content = content.replace(route_target, route_replacement, 1)
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added favicon endpoint to app.py")
else:
    print("Target already updated or not found")
