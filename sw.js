const CACHE = 'londres2026-v4';
const RECURSOS = [
  './',
  'index.html',
  'manifest.webmanifest',
  'sitios.js',
  'img/portada-hero.jpg',
  'img/mapa-londres.jpg',
  'img/brick-lane.jpg',
  'img/gasholder.jpg',
  'img/chinatown.jpg',
  'img/borough.jpg',
  'img/natural-history.jpg',
  'img/greenwich.jpg',
  'img/west-norwood.jpg',
  'img/west-norwood-doulton.jpg',
  'img/icono-192.png',
  'img/icono-512.png',
  'img/portada.jpg',
];


self.addEventListener('install', e => self.skipWaiting());

// La página pide activar la versión nueva sin esperar a cerrar todas las pestañas
self.addEventListener('message', e => {
  if (e.data && e.data.tipo === 'ACTIVAR_YA') self.skipWaiting();
});
self.addEventListener('activate', e => e.waitUntil(
  caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k))))
    .then(() => self.clients.claim())
));

// Cache-first para lo nuestro: una vez guardado, funciona sin conexión.
// Los audios se piden por trozos (cabecera Range). Si están en la caché hay que
// servirlos troceados a mano, o el navegador no deja avanzar ni retroceder la pista.
async function desdeCache(peticion) {
  const guardado = await caches.match(peticion, {ignoreSearch: true});
  const rango = peticion.headers.get('range');
  if (!guardado || !rango) return guardado;

  const datos = await guardado.arrayBuffer();
  const trozos = /bytes=(\d*)-(\d*)/.exec(rango);
  let ini = trozos && trozos[1] ? parseInt(trozos[1], 10) : 0;
  let fin = trozos && trozos[2] ? parseInt(trozos[2], 10) : datos.byteLength - 1;
  if (isNaN(ini) || ini >= datos.byteLength) ini = 0;
  if (isNaN(fin) || fin >= datos.byteLength) fin = datos.byteLength - 1;

  return new Response(datos.slice(ini, fin + 1), {
    status: 206,
    statusText: 'Partial Content',
    headers: {
      'Content-Type': guardado.headers.get('Content-Type') || 'application/octet-stream',
      'Content-Range': 'bytes ' + ini + '-' + fin + '/' + datos.byteLength,
      'Content-Length': String(fin - ini + 1),
      'Accept-Ranges': 'bytes'
    }
  });
}

// La página y el catálogo cambian; las fotos y los audios, no.
// Por eso van con estrategias distintas: si todo fuera cache-first, una vez
// guardada la web nunca se verían las actualizaciones.
function esContenidoVivo(peticion, url) {
  return peticion.mode === 'navigate' ||
         url.pathname.endsWith('/') ||
         url.pathname.endsWith('.html') ||
         url.pathname.endsWith('catalogo.js') ||
         url.pathname.endsWith('sitios.js');
}

function guarda(peticion, resp) {
  if (resp && resp.ok && resp.status === 200) {
    const copia = resp.clone();
    caches.open(CACHE).then(c => c.put(peticion, copia)).catch(() => {});
  }
  return resp;
}

self.addEventListener('fetch', e => {
  const url = new URL(e.request.url);
  if (e.request.method !== 'GET' || url.origin !== location.origin) return;

  if (esContenidoVivo(e.request, url)) {
    // Primero la red, para ver siempre la última versión. Si no hay cobertura,
    // se tira de lo guardado, que es justo lo que hace falta en el viaje.
    e.respondWith(
      fetch(e.request)
        .then(resp => guarda(e.request, resp))
        .catch(() => caches.match(e.request, {ignoreSearch: true})
          .then(hit => hit || caches.match('index.html', {ignoreSearch: true})))
    );
    return;
  }

  // Fotos, audios y demás: de la caché, que no cambian y pesan.
  e.respondWith(
    desdeCache(e.request).then(hit =>
      hit || fetch(e.request)
        .then(resp => guarda(e.request, resp))
        .catch(() => caches.match('index.html', {ignoreSearch: true}))
    )
  );
});

// Descarga completa bajo demanda, informando del progreso.
self.addEventListener('message', async e => {
  if (!e.data || e.data.tipo !== 'GUARDAR') return;
  const cliente = e.source;
  const cache = await caches.open(CACHE);
  let hechos = 0;
  for (const r of RECURSOS) {
    try { await cache.add(new Request(r, {cache: 'reload'})); } catch (err) {}
    hechos++;
    cliente && cliente.postMessage({tipo: 'PROGRESO', hechos, total: RECURSOS.length});
  }
  cliente && cliente.postMessage({tipo: 'LISTO', total: RECURSOS.length});
});
