# Londres 2026 — guía de una semana

Web estática de una sola página, para unos amigos que van a Londres la semana del **29 de agosto
de 2026** con una niña de seis años. No lleva día a día: va por zonas, y cada zona trae sus cosas
que ver y **dónde comer allí mismo**.

Publicada en → https://iaadileli.github.io/viaje-londres-2026/

## Cómo se monta

El `index.html` **no se edita a mano**: se monta juntando las piezas de `generador/plantilla/`.

```bash
python3 generador/comer.py    # datos.py -> plantilla/comer/*.html y sitios.js (geocodifica en Nominatim)
python3 generador/montar.py   # junta las piezas -> index.html
node generador/revisar.mjs    # revisa la página EN MARCHA (obligatorio antes de dar nada por bueno)
python3 hacer-copia.py        # londres-sin-conexion.html, un solo fichero
```

- **`generador/datos.py`** es la fuente única de los 30 sitios de comer: nombre, dirección, sellos,
  qué pedir y horarios. Todo lo demás se genera desde ahí.
- Las coordenadas se piden a Nominatim y se cachean en `generador/datos-fuente/coordenadas.json`.
  Tres locales que Nominatim no tiene van a mano en el diccionario `MANUAL` de `comer.py`.

## Fotos

`generador/fotos.py` busca candidatas en Wikimedia Commons, `hoja-contacto.py` monta hojas de
contacto para **mirarlas** (la búsqueda por texto devuelve bastantes falsos positivos: buscando
«Borough Market» salieron seis fotos del mercado de Sclater Street) y `elegir.py` baja las
elegidas a `img/` y guarda los créditos en `datos-fuente/creditos.json`, que van en el pie.
`portada.py` genera la portada de WhatsApp (1200×630) y los iconos.

## Tres fallos heredados de la plantilla de Nerja, arreglados aquí

Conviene portarlos a `viaje-nerja` y `viaje-tailandia`:

1. **`revisar.mjs` usaba el puerto fijo 8731.** Si quedaba un servidor huérfano de otra guía,
   `spawn` fallaba en silencio y se revisaba **la web equivocada** dando «todo correcto».
   Ahora busca puerto libre y comprueba que lo servido es esta carpeta.
2. **El panel «¿qué tengo cerca?» mostraba `undefined`** como sello: `sitios.js` guardaba las
   letras `a`/`v`/`l`/`b` y el JS y el CSS esperaban `amigo`/`leyenda`/`local`/`barato`.
3. **El sello «lleva décadas abierto» salía enorme**: la clase `leyenda` del `<span>` heredaba
   la caja `.leyenda` del mapa (padding, borde y sombra).

Y en modo oscuro los bloques `.comer` se quedaban con fondo claro y texto claro: corregido en
`css-londres.html`.
