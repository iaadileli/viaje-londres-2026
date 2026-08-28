#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera plantilla/comer/<zona>.html y sitios.js a partir de datos.py.
Las coordenadas se piden a Nominatim y se cachean; ejecutar tras tocar datos.py."""
import json, os, sys, time, urllib.request, urllib.parse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from datos import SITIOS, ZONAS

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(RAIZ)
CACHE = 'generador/datos-fuente/coordenadas.json'
os.makedirs('generador/datos-fuente', exist_ok=True)
os.makedirs('generador/plantilla/comer', exist_ok=True)

SVG = {
 'amigo':  '<path d="M12 21s-7.5-4.7-9.4-9.1C1.2 8.5 3.1 5 6.5 5c2 0 3.5 1.1 4.4 2.4l1.1 1.5 1.1-1.5C14 6.1 15.5 5 17.5 5c3.4 0 5.3 3.5 3.9 6.9C19.5 16.3 12 21 12 21z"/>',
 'leyenda':'<path d="M12 2.6l2.9 5.9 6.5.9-4.7 4.6 1.1 6.5-5.8-3-5.8 3 1.1-6.5L2.6 9.4l6.5-.9z"/>',
 'local':  '<circle cx="12" cy="12" r="6"/>',
 'cena':   '<path d="M7 3v8a3 3 0 0 0 6 0V3M10 11v10M17 3c-1.5 2-2 4-2 6.5 0 1.5.7 2.5 2 2.5v9"/>',
}
TITULO = {'amigo':'te lo recomienda alguien que ha estado', 'leyenda':'lleva décadas abierto',
          'barato':'se come por menos de 12 £', 'local':'donde come la gente de aquí',
          'cena':'la comida buena de la semana'}
# el de «barato» es la etiqueta de precio, con trazo en vez de relleno
BARATO = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linejoin="round">'
          '<path d="M11.5 2.5H20a1.5 1.5 0 0 1 1.5 1.5v8.5L12 21.5 2.5 12z"/>'
          '<circle cx="17" cy="7" r="1.6" fill="currentColor" stroke="none"/></svg>')

def sello(k):
    cuerpo = BARATO if k == 'barato' else \
        '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">%s</svg>' % SVG[k] \
        if k != 'cena' else \
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">%s</svg>' % SVG[k]
    return '<span class="sello %s" title="%s">%s</span>' % (k, TITULO[k], cuerpo)

def maps(consulta):
    return 'https://www.google.com/maps/search/?api=1&query=' + urllib.parse.quote(consulta)

# ---------------------------------------------------------------- coordenadas
# Nominatim no tiene estos tres locales; van a mano, a pie de portal (error < 50 m)
MANUAL = {
 'Boulangerie Jade, Major Draper Street, Woolwich, London': [51.493300, 0.070500, 0],
 'Blue Nile, 73 Woolwich New Road, London':                 [51.488990, 0.067360, 0],
 'Station Kebab House, Vincent Road, London':               [51.489900, 0.069900, 0],
 'Poppies Fish and Chips, 6 Hanbury Street, London': [51.519930, -0.074130, 0],
 'Bleecker Burger, Old Spitalfields Market, London': [51.519650, -0.075330, 0],
 'Dishoom Shoreditch, 7 Boundary Street, London':      [51.524499, -0.076825, 0],
 'Dishoom Kings Cross, 5 Stable Street, London':     [51.535420, -0.126380, 0],
}
coords = json.load(open(CACHE)) if os.path.exists(CACHE) else {}
coords.update({k: v for k, v in MANUAL.items() if not coords.get(k)})
def geo(consulta):
    if consulta in coords:
        return coords[consulta]
    url = ('https://nominatim.openstreetmap.org/search?' +
           urllib.parse.urlencode({'q': consulta, 'format': 'json', 'limit': 1}))
    req = urllib.request.Request(url, headers={'User-Agent': 'guia-londres/1.0 (uso personal)'})
    try:
        r = json.load(urllib.request.urlopen(req, timeout=20))
        if r:
            coords[consulta] = [round(float(r[0]['lat']), 6), round(float(r[0]['lon']), 6), 0]
            print('  ✓ %s' % consulta)
        else:
            coords[consulta] = None
            print('  ✗ SIN COORDENADAS: %s' % consulta)
    except Exception as e:
        coords[consulta] = None
        print('  ✗ error (%s): %s' % (e, consulta))
    time.sleep(1.1)   # Nominatim pide máximo una petición por segundo
    return coords[consulta]

print('Geocodificando %d sitios…' % len(SITIOS))
for s in SITIOS:
    geo(s['geo'])
json.dump(coords, open(CACHE, 'w'), ensure_ascii=False, indent=1)

# ------------------------------------------------------------- bloques comer
LEYENDA = ('  <div class="leyenda-sellos">' +
  ''.join('<span><i style="background:%s">%s</i>%s</span>' % (color, cuerpo, TITULO[k])
          for k, color, cuerpo in [
            ('amigo',   '#a8386b', '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">%s</svg>' % SVG['amigo']),
            ('leyenda', 'var(--teca)', '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">%s</svg>' % SVG['leyenda']),
            ('barato',  'var(--mar)', BARATO),
            ('local',   'var(--verde)', '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">%s</svg>' % SVG['local']),
          ]) + '</div>\n')

for zona, (titulo, platos) in ZONAS.items():
    de_zona = [s for s in SITIOS if s['z'] == zona]
    h = ['  <div class="comer">', '    <h3>%s</h3>' % titulo, '    <div class="platos">']
    h.append('      ' + ''.join('<span class="plato">%s</span>' % p for p in platos))
    h += ['    </div>', '    <ul class="sitios">']
    for s in de_zona:
        h.append('      <li><span class="nombre">%s</span>%s — <span class="dir">%s</span> · %s'
                 % (s['n'], ''.join(sello(k) for k in s['s']), s['dir'], s['t']))
        h.append('        <span class="pedir"><b>Pedid</b> %s</span>' % s['p'])
        h.append('        <span class="datos">%s</span>' % s['d'])
        h.append('        <a href="%s" target="_blank" rel="noopener">📍 Maps</a></li>' % maps(s['geo']))
    h += ['    </ul>', '  </div>']
    open('generador/plantilla/comer/%s.html' % zona, 'w').write('\n'.join(h) + '\n')
    print('comer/%s.html · %d sitios' % (zona, len(de_zona)))

open('generador/plantilla/comer/leyenda.html', 'w').write(LEYENDA)

# ----------------------------------------------------------------- sitios.js
ETIQUETA = {'woolwich':'Woolwich (vuestro barrio)', 'este':'Brick Lane y Shoreditch', 'kingscross':"King's Cross", 'soho':'Soho y Covent Garden',
            'sur':'Borough y la orilla sur', 'museos':'South Kensington', 'greenwich':'Greenwich'}
js = []
faltan = []
for s in SITIOS:
    c = coords.get(s['geo'])
    if not c:
        faltan.append(s['n']); continue
    principal = ([k for k in s['s'] if k != 'amigo'] + [k for k in s['s'] if k == 'amigo'] + [''])[0]
    js.append({'n': s['n'], 'z': s['dir'].split(' · ')[0], 'e': ETIQUETA[s['z']],
               's': principal, 'la': c[0], 'lo': c[1], 'ap': c[2],
               'q': urllib.parse.quote(s['geo'])})
open('sitios.js', 'w').write('const SITIOS=' + json.dumps(js, ensure_ascii=False, separators=(',', ':')) + ';\n')
print('sitios.js · %d sitios situados%s' % (len(js), (', SIN COORDENADAS: ' + ', '.join(faltan)) if faltan else ''))
