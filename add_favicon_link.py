with open('static/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

target = '<title>DECK - Historical Log &amp; Telemetry Intelligence</title>'
replacement = '<title>DECK - Historical Log &amp; Telemetry Intelligence</title>\n  <link rel="icon" type="image/svg+xml" href="/favicon.ico">'

if target in text:
    text = text.replace(target, replacement, 1)
    with open('static/index.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print('Added favicon link to static/index.html')
