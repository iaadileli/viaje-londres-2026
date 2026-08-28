#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Compone el mapa de la guía: un MAPA DE VERDAD de fondo (teselas de
OpenStreetMap) con las zonas encima, cada una en su coordenada real.
Genera img/mapa-londres.jpg y generador/plantilla/c3-mapa.html.
OSM es ODbL: la atribución «© OpenStreetMap» va en el pie del mapa."""
import math, os, time, urllib.request
from PIL import Image, ImageEnhance

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
UA = 'guia-viaje-londres/1.0 (uso personal, una sola composicion)'
ZOOM = 13
# el recorte: entra West Norwood por abajo, Greenwich por la derecha y Notting Hill por la izquierda
OESTE, ESTE = -0.245, 0.108
SUR, NORTE  = 51.420, 51.556

# zona -> (lat, lon, sección, título, subtítulo, destacada, dónde va la etiqueta)
ZONAS = [
 (51.4936,  0.0702, '#woolwich',   'WOOLWICH',                'vuestra casa',             True,  'arriba'),
 (51.5090, -0.1960, '#carnaval',   'Notting Hill',            'el carnaval',              False, 'arriba'),
 (51.4941, -0.1738, '#museos',     'South Kensington',        'los museos grandes',       True,  'abajo'),
 (51.5414, -0.1460, '#paseos',     'Camden',                  'canal y mercado',          False, 'arriba'),
 (51.5308, -0.1238, '#kingscross', 'King’s Cross',            'gasómetros y andén 9¾',    True,  'arriba'),
 (51.5129, -0.1300, '#soho',       'Soho · Covent Garden',    'Chinatown y Japan Centre', True,  'abajo'),
 (51.5240, -0.0720, '#este',       'Brick Lane · Shoreditch', 'comer y mercados',         True,  'arriba'),
 (51.5138, -0.0870, '#paseos',     'la City',                 'Sky Garden y Leadenhall',  False, 'derecha'),
 (51.5050, -0.0900, '#sur',        'Borough · South Bank',    'mercado y la Tate',        True,  'abajo'),
 (51.4816, -0.0090, '#greenwich',  'Greenwich',               'en barco desde el centro', True,  'arriba'),
 (51.4310, -0.0980, '#paseos',     'West Norwood',            'el cementerio victoriano', False, 'arriba'),
]

def x_tile(lon, z): return (lon + 180.0) / 360.0 * 2**z
def y_tile(lat, z):
    r = math.radians(lat)
    return (1.0 - math.log(math.tan(r) + 1/math.cos(r)) / math.pi) / 2.0 * 2**z

x0f, x1f = x_tile(OESTE, ZOOM), x_tile(ESTE, ZOOM)
y0f, y1f = y_tile(NORTE, ZOOM), y_tile(SUR, ZOOM)
x0, x1 = math.floor(x0f), math.ceil(x1f)
y0, y1 = math.floor(y0f), math.ceil(y1f)
ancho_t, alto_t = x1 - x0, y1 - y0
print('teselas: %d x %d = %d (zoom %d)' % (ancho_t, alto_t, ancho_t * alto_t, ZOOM))

cache = 'generador/datos-fuente/teselas'
os.makedirs(cache, exist_ok=True)
lienzo = Image.new('RGB', (ancho_t * 256, alto_t * 256), '#e8eef6')
bajadas = 0
for tx in range(x0, x1):
    for ty in range(y0, y1):
        ruta = '%s/%d-%d-%d.png' % (cache, ZOOM, tx, ty)
        if not os.path.exists(ruta):
            url = 'https://tile.openstreetmap.org/%d/%d/%d.png' % (ZOOM, tx, ty)
            req = urllib.request.Request(url, headers={'User-Agent': UA})
            with urllib.request.urlopen(req, timeout=30) as r, open(ruta, 'wb') as f:
                f.write(r.read())
            bajadas += 1
            time.sleep(0.4)
        lienzo.paste(Image.open(ruta).convert('RGB'), ((tx - x0) * 256, (ty - y0) * 256))
print('teselas descargadas ahora:', bajadas, '· el resto, de la caché')

# recorte exacto al trozo que interesa
izq   = round((x0f - x0) * 256)
arr   = round((y0f - y0) * 256)
der   = round((x1f - x0) * 256)
abajo = round((y1f - y0) * 256)
mapa = lienzo.crop((izq, arr, der, abajo))
W, H = mapa.size
print('mapa recortado: %dx%d px' % (W, H))

# se aclara y desatura para que las etiquetas se lean por encima
mapa = ImageEnhance.Color(mapa).enhance(0.55)
mapa = Image.blend(mapa, Image.new('RGB', mapa.size, 'white'), 0.28)
mapa.save('img/mapa-londres.jpg', 'JPEG', quality=84, optimize=True, progressive=True)
print('img/mapa-londres.jpg · %d KB' % (os.path.getsize('img/mapa-londres.jpg') // 1024))

# ---- coordenadas de cada zona dentro de la imagen
def a_pixel(lat, lon):
    return ((x_tile(lon, ZOOM) - x0f) * 256, (y_tile(lat, ZOOM) - y0f) * 256)

puntos = []
for lat, lon, dest, titulo, sub, destaca, donde in ZONAS:
    px, py = a_pixel(lat, lon)
    assert 0 <= px <= W and 0 <= py <= H, 'fuera del mapa: %s' % titulo
    puntos.append((px, py, dest, titulo, sub, destaca, donde))
    print('  %-24s %6.0f, %6.0f  (%s)' % (titulo, px, py, donde))

# ---------------------------------------------------------------- el SVG
def escapa(t):
    return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

filas = []
for px, py, dest, titulo, sub, destaca, donde in puntos:
    r = 15 if destaca else 12
    if donde == 'arriba':
        tx, ty, sy, anclaje = px, py - 34, py - 12, 'middle'
    elif donde == 'abajo':
        tx, ty, sy, anclaje = px, py + 44, py + 68, 'middle'
    elif donde == 'izquierda':
        tx, ty, sy, anclaje = px - 26, py + 2, py + 26, 'end'
    else:                                     # derecha
        tx, ty, sy, anclaje = px + 26, py + 2, py + 26, 'start'
    ancho = 26 + 15 * len(titulo)
    if anclaje == 'middle':   rx = tx - ancho / 2
    elif anclaje == 'end':    rx = tx - ancho
    else:                     rx = tx
    ry = min(ty, py) - 32
    rh = max(sy, py) - ry + 18
    clase = ' casa' if titulo == 'WOOLWICH' else (' destaca' if destaca else '')
    filas.append(
      '''    <a class="m-punto%s" href="%s" aria-label="Ir a %s">
      <rect class="m-toca" x="%.0f" y="%.0f" width="%.0f" height="%.0f" rx="14"/>
      <circle cx="%.0f" cy="%.0f" r="%d"/>
      <text class="m-tit" x="%.0f" y="%.0f" text-anchor="%s">%s</text>
      <text class="m-sub" x="%.0f" y="%.0f" text-anchor="%s">%s</text>
    </a>''' % (clase, dest, escapa(titulo.replace('·', 'y')),
                min(rx, px - r - 6), ry, max(ancho, 2 * r + 12), rh,
                px, py, r, tx, ty, anclaje, escapa(titulo), tx, sy, anclaje, escapa(sub)))

html = '''
<section id="mapa" class="etapa-sec">
  <div class="kicker">Para hacerse el mapa mental</div>
  <h2>Dónde está cada cosa</h2>
  <p class="intro">Londres se entiende con el río. Todo lo que os interesa está a un lado o al otro
  del Támesis y, salvo Greenwich, dentro de las zonas 1 y 2: <strong>de punta a punta son 30 o 40
  minutos de metro</strong>. Cada chincheta está en su sitio de verdad, y <strong>si la pulsáis os
  lleva a su apartado</strong>.</p>

  <div class="mapa-wrap">
  <svg viewBox="0 0 %d %d" class="mapa-svg" role="img"
       aria-label="Mapa de Londres con las zonas de la guía señaladas; cada una es un enlace a su apartado">
    <image class="m-base" href="img/mapa-londres.jpg" xlink:href="img/mapa-londres.jpg"
           x="0" y="0" width="%d" height="%d" preserveAspectRatio="xMidYMid slice"/>
%s
  </svg>
  </div>

  <div class="mapa-pie sans">
    <span><i class="m-ll destaca"></i>las seis zonas de la guía</span>
    <span><i class="m-ll"></i>otros sitios que se nombran</span>
    <span class="mapa-pinchar"><b>👆 Pulsad en una zona</b> y os lleva a ella</span>
    <span class="mapa-credito">Mapa: <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener">© OpenStreetMap</a></span>
  </div>

  <div class="tip"><b>La regla que os ahorra tiempo:</b> si dos planes están en zonas distintas,
  no los juntéis el mismo día. Un museo del oeste por la mañana y una cena en el este por la noche
  suena bien y son cuarenta minutos de metro en medio, con Julia cansada. Mejor una zona por día
  y andar mucho dentro de ella.</div>

  <div class="cerca-invita sans">
    <b>📍 ¿Y qué tengo cerca ahora mismo?</b> Abajo del todo hay un botón que usa el GPS del móvil
    y os ordena por distancia todos los sitios de comer de esta guía. Sirve para el momento
    «son las dos, tenemos hambre y estamos aquí».
  </div>
</section>
''' % (W, H, W, H, chr(10).join(filas))

open('generador/plantilla/c3-mapa.html', 'w').write(html)
print('generador/plantilla/c3-mapa.html · %d zonas sobre el mapa' % len(puntos))
