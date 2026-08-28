#!/usr/bin/env python3
"""Genera la copia sin conexión: un solo fichero, sin depender de red ni de service worker."""
import re, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
h = open('index.html').read()

# los scripts externos, dentro
for f in ['sitios.js']:
    h = h.replace(f'<script src="{f}"></script>', '<script>\n' + open(f).read() + '</script>')

# sin service worker: aquí no hay servidor que lo sirva.
# En vez de cortar el bloque (que rompía la sintaxis), se desactiva su condición.
v = "} else if ('serviceWorker' in navigator) {"
n = "} else if (false) {  /* copia sin conexión: sin service worker */"
assert v in h, 'no encontré la condición del service worker'
h = h.replace(v, n, 1)

aviso = ('<div style="background:#b4552d;color:#fff;padding:13px 18px;'
         'font-family:-apple-system,\'Segoe UI\',sans-serif;font-size:.9rem;line-height:1.5">'
         '<b>📴 Copia sin conexión</b> — funciona en modo avión, y el «¿qué tengo cerca?» también: '
         'el GPS no necesita datos. La versión que se actualiza está en '
         'iaadileli.github.io/viaje-londres-2026</div>\n')
h = h.replace('<nav class="sans">', aviso + '<nav class="sans">', 1)
h = h.replace('<title>', '<title>[SIN CONEXIÓN] ', 1)
open('londres-sin-conexion.html','w').write(h)
print(f'copia autónoma: {len(h)/1024:.0f} KB · sin service worker ✓')
