#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Busca en Wikimedia Commons las fotos de la guía y deja los candidatos en
datos-fuente/fotos.json. Hay que MIRARLAS (hoja-contacto.py) antes de elegir:
la búsqueda por texto devuelve logos, mapas y fotos sin relación."""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from buscafotos import buscar
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.makedirs('generador/datos-fuente', exist_ok=True)

BUSQUEDAS = {
 'portada-hero':   'Tower Bridge London river Thames skyline',
 'brick-lane':     'Brick Lane London street',
 'gasholder':      'Gasholder Park King\'s Cross London',
 'chinatown':      'Chinatown London Gerrard Street lanterns',
 'borough':        'Borough Market London stalls',
 'natural-history':'Natural History Museum London Hintze Hall',
 'greenwich':      'Cutty Sark Greenwich London',
 'west-norwood':   'West Norwood Cemetery London monuments',
}
res = {}
for k, q in BUSQUEDAS.items():
    r = buscar(q, 8)
    res[k] = r
    print('  %-16s %d · %s' % (k, len(r), (r[0]['t'][5:60] + '  [' + r[0]['lic'] + ']') if r else '— sin resultado'))
    time.sleep(0.5)
json.dump(res, open('generador/datos-fuente/fotos.json', 'w'), ensure_ascii=False, indent=1)
print('\nCandidatos en generador/datos-fuente/fotos.json · ahora: python3 generador/hoja-contacto.py')
