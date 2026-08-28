#!/usr/bin/env bash
# Actualiza la predicción del tiempo de la guía de Londres y la publica.
# Lo llama un hook de Claude al arrancar la sesión, y SE APAGA SOLO
# cuando termina el viaje: a partir del 6 de septiembre de 2026 no hace nada.
set -uo pipefail
cd "$(dirname "$0")" || exit 0

FIN="2026-09-06"
HOY=$(date +%F)
[[ "$HOY" > "$FIN" || "$HOY" == "$FIN" ]] && { echo "El viaje ya ha terminado: no toco nada."; exit 0; }

# una vez al día es suficiente; si ya se hizo hoy, no se repite
SELLO=".ultima-actualizacion-tiempo"
[[ -f "$SELLO" && "$(cat "$SELLO")" == "$HOY" ]] && { echo "El tiempo ya se actualizó hoy."; exit 0; }

python3 generador/tiempo.py || { echo "No he podido consultar la predicción (¿sin red?). Lo dejo como estaba."; exit 0; }
python3 generador/montar.py  || exit 0
python3 hacer-copia.py       || exit 0

if git diff --quiet -- index.html generador/plantilla/d0-tiempo.html; then
  echo "La predicción no ha cambiado."
else
  git add -A
  git -c user.email=type.team@grupo-sm.com -c user.name="Adil" \
      commit -q -m "Predicción del tiempo al día ($HOY)"
  git push -q origin master && echo "Tiempo actualizado y publicado."
fi
echo "$HOY" > "$SELLO"
