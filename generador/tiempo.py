#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Predicción diaria de Londres para los días del viaje.
Genera generador/plantilla/d0-tiempo.html con los datos ya puestos (para que la
web sirva sin conexión y sin depender de que la API responda) y luego el JS de
la página la refresca en vivo al abrirla. Fuente: Open-Meteo, sin clave.
Uso:  python3 generador/tiempo.py   (y después montar.py, que lo hace solo con --montar)"""
import json, os, sys, urllib.request, datetime

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PRIMER, ULTIMO = '2026-08-29', '2026-09-05'          # los días que están en Londres
API = ('https://api.open-meteo.com/v1/forecast?latitude=51.5074&longitude=-0.1278'
       '&daily=weather_code,temperature_2m_max,temperature_2m_min,'
       'precipitation_probability_max,precipitation_sum,wind_speed_10m_max,sunrise,sunset'
       '&timezone=Europe%2FLondon&forecast_days=10')

# código WMO -> (emoji, cómo se dice)
CIELO = {0:('☀️','despejado'), 1:('🌤️','casi despejado'), 2:('⛅','nubes y claros'), 3:('☁️','nublado'),
         45:('🌫️','niebla'), 48:('🌫️','niebla helada'),
         51:('🌦️','llovizna'), 53:('🌦️','llovizna'), 55:('🌧️','llovizna fuerte'),
         56:('🌧️','llovizna helada'), 57:('🌧️','llovizna helada'),
         61:('🌦️','lluvia floja'), 63:('🌧️','lluvia'), 65:('🌧️','lluvia fuerte'),
         66:('🌧️','lluvia helada'), 67:('🌧️','lluvia helada'),
         71:('🌨️','nieve'), 73:('🌨️','nieve'), 75:('🌨️','nieve fuerte'), 77:('🌨️','granizo menudo'),
         80:('🌦️','chubascos'), 81:('🌧️','chubascos'), 82:('🌧️','chubascos fuertes'),
         85:('🌨️','chubascos de nieve'), 86:('🌨️','chubascos de nieve'),
         95:('⛈️','tormenta'), 96:('⛈️','tormenta con granizo'), 99:('⛈️','tormenta con granizo')}
SEMANA = ['lunes','martes','miércoles','jueves','viernes','sábado','domingo']
MESES = ['enero','febrero','marzo','abril','mayo','junio','julio','agosto',
         'septiembre','octubre','noviembre','diciembre']

d = json.load(urllib.request.urlopen(urllib.request.Request(API, headers={'User-Agent':'guia-londres/1.0'}), timeout=25))['daily']
dias = []
for i, fecha in enumerate(d['time']):
    if not (PRIMER <= fecha <= ULTIMO):
        continue
    f = datetime.date.fromisoformat(fecha)
    cod = d['weather_code'][i]
    emoji, texto = CIELO.get(cod, ('🌡️', 'variable'))
    dias.append({
        'f': fecha,
        'dia': '%s %d' % (SEMANA[f.weekday()], f.day),
        'mes': MESES[f.month - 1],
        'e': emoji, 't': texto,
        'max': round(d['temperature_2m_max'][i]), 'min': round(d['temperature_2m_min'][i]),
        'lluvia': d['precipitation_probability_max'][i] or 0,
        'mm': d['precipitation_sum'][i] or 0,
        'viento': round(d['wind_speed_10m_max'][i]),
        'sale': d['sunrise'][i][11:16], 'pone': d['sunset'][i][11:16],
    })
if not dias:
    sys.exit('La API no ha devuelto ninguno de los días del viaje (%s a %s)' % (PRIMER, ULTIMO))

hoy = datetime.date.today()
actualizado = '%d de %s' % (hoy.day, MESES[hoy.month - 1])
mojados = [x for x in dias if x['lluvia'] >= 50]
maxima = max(x['max'] for x in dias)
minima = min(x['min'] for x in dias)

if not mojados:
    resumen = ('Ni un solo día con la lluvia por encima del 50 %. Aun así, en Londres cae un '
               'chaparrón de media hora sin avisar: el chubasquero, en la mochila.')
elif len(mojados) <= 2:
    resumen = ('Solo %s con probabilidad alta de lluvia. Ese día es el bueno para meterse en '
               '<a href="#museos">los museos</a> o en el <a href="#lluvia">plan de días feos</a>.'
               % (' y '.join(x['dia'] for x in mojados)))
else:
    resumen = ('Varios días con lluvia probable (%s). No pasa nada: cae media hora y escampa. '
               'Chubasquero con capucha mejor que paraguas, que con el viento no sirve.'
               % ', '.join(x['dia'] for x in mojados))

# el carnaval es al aire libre y son los tres primeros días: si moja, hay que decirlo
carnaval = [x for x in dias if x['f'] in ('2026-08-29', '2026-08-30', '2026-08-31') and x['lluvia'] >= 50]
if carnaval:
    resumen += (' <b>Ojo al fin de semana del <a href="#carnaval">carnaval</a></b>, que es todo en '
                'la calle: %s. Con Julia, chubasquero puesto desde casa y calzado cerrado.'
                % ', '.join('%s al %d%%' % (x['dia'], x['lluvia']) for x in carnaval))

filas = []
for x in dias:
    clase = ' mojado' if x['lluvia'] >= 50 else ''
    filas.append(
'''      <div class="t-dia%s" data-t="%s">
        <div class="t-cuando"><b>%s</b><span>de %s</span></div>
        <div class="t-icono" aria-hidden="true">%s</div>
        <div class="t-cielo">%s</div>
        <div class="t-grados"><b>%d°</b><span>%d°</span></div>
        <div class="t-lluvia">💧 %d%%</div>
        <div class="t-viento">💨 %d km/h</div>
      </div>''' % (clase, x['f'], x['dia'], x['mes'], x['e'], x['t'], x['max'], x['min'], x['lluvia'], x['viento']))

html = '''
<section id="tiempo" class="etapa-sec">
  <div class="kicker">Qué meter en la maleta</div>
  <h2>El tiempo, día a día</h2>
  <p class="intro">%s</p>

  <div class="tiempo-rejilla" id="tiempoRejilla">
%s
  </div>

  <div class="t-pie sans">
    <span id="tiempoSello">Predicción del %s · se actualiza sola al abrir la web</span>
    <span>🌅 amanece a las %s · 🌇 anochece a las %s</span>
    <span>Máximas de %d° a %d° · mínimas de hasta %d°</span>
  </div>

  <div class="tip"><b>Con esos números:</b> manga corta de día y <b>una chaqueta fina para la
  noche</b>, que en cuanto se pone el sol refresca. Calzado cómodo y que aguante un charco. Y para
  Julia, una capa impermeable con capucha: los paraguas en Londres duran lo que dura la primera
  racha de viento.</div>
</section>
''' % (resumen, '\n'.join(filas), actualizado, dias[0]['sale'], dias[0]['pone'], minima, maxima, minima)

open('generador/plantilla/d0-tiempo.html', 'w').write(html)
print('d0-tiempo.html · %d días (%s a %s) · máx %d° · mín %d° · %d día(s) de lluvia probable'
      % (len(dias), dias[0]['dia'], dias[-1]['dia'], maxima, minima, len(mojados)))
