#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Copia a img/ las fotos elegidas a mano tras mirar las hojas de contacto,
y deja en datos-fuente/creditos.json el título, autor y licencia de cada una
(las de Wikimedia son CC BY / CC BY-SA: hay que citarlas)."""
import json, os, subprocess, time, urllib.parse
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
UA = 'guia-viaje-londres/1.0 (uso personal)'

# destino -> (fichero de candidatos, clave, índice elegido)
ELEGIDAS = {
 'portada-hero':    ('fotos.json',  'portada-hero',    3),
 'brick-lane':      ('fotos.json',  'brick-lane',      2),
 'gasholder':       ('fotos.json',  'gasholder',       0),
 'chinatown':       ('fotos.json',  'chinatown',       3),
 'borough':         ('fotos.json',  'borough',         0),
 'natural-history': ('fotos.json',  'natural-history', 3),
 'greenwich':       ('fotos2.json', 'greenwich3',      2),
 'west-norwood':    ('fotos.json',  'west-norwood',    3),
}
creditos = {}
for destino, (fich, clave, idx) in ELEGIDAS.items():
    c = json.load(open('generador/datos-fuente/' + fich))[clave][idx]
    # se vuelve a pedir en 1600 px de ancho para que el hero no salga pixelado
    url = c['url'].replace('/1100px-', '/1600px-')
    ruta = 'img/%s.jpg' % destino
    subprocess.run(['curl','-sL','--max-time','60','-A',UA,'-o',ruta,url], check=False)
    if not os.path.exists(ruta) or os.path.getsize(ruta) < 5000:
        subprocess.run(['curl','-sL','--max-time','60','-A',UA,'-o',ruta,c['url']], check=False)
    creditos[destino] = {'titulo': c['t'][5:], 'licencia': c['lic'],
                         'pagina': 'https://commons.wikimedia.org/wiki/' + urllib.parse.quote(c['t'].replace(' ', '_'))}
    print('  %-16s %6d KB  [%s]  %s' % (destino, os.path.getsize(ruta)//1024, c['lic'], c['t'][5:55]))
    time.sleep(0.5)
json.dump(creditos, open('generador/datos-fuente/creditos.json','w'), ensure_ascii=False, indent=1)
print('\nCréditos en generador/datos-fuente/creditos.json')
