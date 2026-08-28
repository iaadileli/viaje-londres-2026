#!/usr/bin/env python3
"""Monta index.html juntando las piezas de generador/plantilla/ e inyectando los
bloques de comida dentro de la sección de su zona (el «qué tengo cerca» y los
contadores buscan los .sitios dentro de la sección, no en una sección aparte)."""
import re, os
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(RAIZ)
P = 'generador/plantilla/'

PIEZAS = ['head-nuevo.html', 'css-base.html', 'css-londres.html', 'c1-cabecera.html', 'c2-carnaval.html',
          'c0-woolwich.html', 'd0-tiempo.html', 'c3-mapa.html', 'c4-este.html', 'c5-kingscross.html', 'c6-soho.html',
          'c7-sur.html', 'c8-museos.html', 'c9-greenwich.html', 'd1-nina.html',
          'd2-paseos.html', 'd3-comer.html', 'd4-entradas.html', 'd5-transporte.html',
          'd6-practico.html', 'd7-offline.html', 'd8-footer.html', 'js-tiempo.html', '3-scripts.html']
# id de la sección de la web -> fichero de comida
COMIDA = {'woolwich': 'woolwich', 'este': 'este', 'kingscross': 'kingscross', 'soho': 'soho',
          'sur': 'sur', 'museos': 'museos', 'greenwich': 'greenwich'}

leyenda = open(P + 'comer/leyenda.html').read()
puesta = False
partes = []
for pieza in PIEZAS:
    s = open(P + pieza).read()
    for sec, fich in COMIDA.items():
        marca = '<section id="%s" class="etapa-sec">' % sec
        if marca not in s:
            continue
        bloque = open(P + 'comer/%s.html' % fich).read()
        pon = ('' if puesta else leyenda) + bloque
        puesta = True
        pat = re.compile(r'(<section id="%s" class="etapa-sec">.*?)(</section>)' % sec, re.S)
        s, n = pat.subn(lambda m: m.group(1) + '\n' + pon + m.group(2), s, count=1)
        assert n == 1, 'no se pudo inyectar la comida en #' + sec
    partes.append(s)

html = ''.join(partes)
html = html.replace('</style>\n<body>', '</style>\n</head>\n<body>', 1)
if not html.rstrip().endswith('</html>'):
    html = html.rstrip() + '\n</html>\n'
open('index.html', 'w').write(html)
print('index.html montado: %d KB · %d sitios de comer' % (len(html) // 1024, html.count('<li><span class="nombre">')))
