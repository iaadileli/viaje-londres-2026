#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Copia a img/ las fotos elegidas a mano tras mirar las hojas de contacto.
El tamaño se le PIDE A LA API (iiurlwidth); manipular la url del thumb a mano
no funciona y dejaba fotos de 1280 px donde el original tenía 13.000.
Deja el título, autor y licencia en datos-fuente/creditos.json: son CC BY / BY-SA
y hay que citarlas."""
import json, os, subprocess, time, urllib.parse
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
UA = 'guia-viaje-londres/1.0 (uso personal)'

# destino -> (fichero de candidatos, clave, índice elegido, ancho que se pide)
ELEGIDAS = {
 'portada-hero':    ('fotos.json',  'portada-hero',    3, 2400),
 'brick-lane':      ('fotos.json',  'brick-lane',      2, 1600),
 'gasholder':       ('fotos.json',  'gasholder',       0, 1600),
 'chinatown':       ('fotos.json',  'chinatown',       3, 1600),
 'borough':         ('fotos5.json', 'bm2',             9, 1600),
 'natural-history': ('fotos.json',  'natural-history', 3, 1600),
 'greenwich':       ('fotos2.json', 'greenwich3',      2, 1600),
 'west-norwood':    ('fotos.json',  'west-norwood',    3, 1600),
}

def thumb(titulo, ancho):
    """URL del thumb del ancho pedido (o del original si es más pequeño)."""
    cmd = ['curl','-s','--max-time','30','-G','https://commons.wikimedia.org/w/api.php','-A',UA,
           '--data-urlencode','action=query','--data-urlencode','titles='+titulo,
           '--data-urlencode','prop=imageinfo','--data-urlencode','iiprop=url|size|extmetadata',
           '--data-urlencode','iiurlwidth=%d' % ancho,'--data-urlencode','format=json']
    d = json.loads(subprocess.run(cmd, capture_output=True, text=True).stdout or '{}')
    p = list(d.get('query', {}).get('pages', {}).values())[0]
    i = p['imageinfo'][0]
    m = i.get('extmetadata', {})
    return (i.get('thumburl') or i['url'], i['width'],
            m.get('LicenseShortName', {}).get('value', '?'),
            m.get('Artist', {}).get('value', ''))

import re
creditos = {}
for destino, (fich, clave, idx, ancho) in ELEGIDAS.items():
    c = json.load(open('generador/datos-fuente/' + fich))[clave][idx]
    url, ancho_original, lic, autor = thumb(c['t'], ancho)
    ruta = 'img/%s.jpg' % destino
    subprocess.run(['curl','-sL','--max-time','90','-A',UA,'-o',ruta,url], check=False)
    autor = re.sub(r'<[^>]+>', '', autor).strip()[:60]
    creditos[destino] = {'titulo': c['t'][5:], 'licencia': lic, 'autor': autor,
                         'pagina': 'https://commons.wikimedia.org/wiki/' + urllib.parse.quote(c['t'].replace(' ', '_'))}
    from PIL import Image
    w, h = Image.open(ruta).size
    forma = 'apaisada' if w > h * 1.15 else ('VERTICAL: se recorta fatal en el banner' if h > w else 'cuadrada')
    print('  %-16s %6d KB  %dx%d  %s  [%s]' %
          (destino, os.path.getsize(ruta)//1024, w, h, forma, lic))
    time.sleep(0.6)
json.dump(creditos, open('generador/datos-fuente/creditos.json','w'), ensure_ascii=False, indent=1)
print('\nCréditos en generador/datos-fuente/creditos.json')
