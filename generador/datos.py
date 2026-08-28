#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fuente única de los sitios de comer de Londres.
Genera generador/plantilla/comer/<zona>.html y sitios.js (el «qué tengo cerca»).
Las coordenadas se piden a Nominatim y se cachean en datos-fuente/coordenadas.json."""

# sellos: amigo (lo recomienda alguien que ha estado), leyenda (lleva décadas),
#         barato (se come por menos de 12 £), local (donde come la gente de aquí),
#         cena (para la comida buena de la semana)

ZONAS = {
 'este':      ('Qué y dónde comer en Brick Lane y Shoreditch',
               ['Beigel de salt beef', 'Brisket ahumado', 'Curry punyabí', 'Hamburguesa',
                'Fish and chips', 'Bacon naan', 'Desayuno inglés']),
 'kingscross':('Qué y dónde comer en King’s Cross',
               ['Desayuno indio', 'Roti canai', 'Brunch', 'Tacos']),
 'soho':      ('Qué y dónde comer en Soho, Chinatown y Covent Garden',
               ['Sushi rebajado', 'Bao al vapor', 'Dim sum', 'Filete a precio fijo', 'Café italiano']),
 'sur':       ('Qué y dónde comer en Borough y la orilla sur',
               ['Grilled cheese', 'Pasta fresca', 'Donuts', 'Ostras', 'Cerveza en pub del XVII']),
 'museos':    ('Qué y dónde comer en South Kensington',
               ['Picnic en el parque', 'Comida japonesa', 'Té con pastas']),
 'greenwich': ('Qué y dónde comer en Greenwich',
               ['Pie and mash', 'Puestos del mercado', 'Pub junto al río']),
}

SITIOS = [
# ---------------------------------------------------------------- EL ESTE
 dict(z='este', n='Beigel Bake', s=['amigo','leyenda','barato'],
   dir='159 Brick Lane, E1 6SB · la puerta amarilla',
   geo='Beigel Bake, 159 Brick Lane, London',
   t='El sitio. Una panadería estrecha con luz de fluorescente, abierta <b>24 horas los 365 días</b> '
     'desde 1974, donde siempre hay cola y siempre va rápido. Piden a gritos el pedido, cortan el '
     '<i>salt beef</i> a cuchillo delante de vosotros y os lo meten en un beigel hervido. Es de las '
     'pocas cosas que quedan del Londres judío del East End.',
   p='Un <b>salt beef beigel with mustard and pickle</b>. Si no queréis mostaza inglesa, decidlo: pica de verdad',
   d='🕐 abierto 24 h · 💷 unas 8–9 £ el beigel de carne, y menos de 2 £ los de queso · efectivo y tarjeta'),
 dict(z='este', n='The Beigel Shop', s=['leyenda','barato'],
   dir='155 Brick Lane, E1 6QL · la puerta blanca, dos portales antes',
   geo='Beigel Shop, 155 Brick Lane, London',
   t='La de al lado, la rival de toda la vida. Presume de ser la primera panadería de beigels de '
     'Brick Lane y las dos familias fueron la misma. Los londinenses se pelean por cuál es mejor y '
     'la respuesta honesta es que están igual de buenas.',
   p='Lo mismo que en la otra, para poder opinar. O el beigel de <b>arenque</b>, que allí no siempre hay',
   d='🕐 24 h · 💷 igual de barato · si en una hay veinte de cola y en la otra cinco, la respuesta es fácil'),
 dict(z='este', n='Smokestak', s=['amigo','cena'],
   dir='35 Sclater Street, E1 6LB · a dos calles de Brick Lane',
   geo='Smokestak, 35 Sclater Street, London',
   t='Barbacoa en un arco de ferrocarril: paredes negras, mucho humo y <b>brisket ahumado doce o '
     'quince horas sobre leña de roble</b>. Empezó siendo un puesto de mercado. Es la comida más '
     'seria de esta lista y aun así se come con las manos.',
   p='El <b>brisket bun</b> con encurtidos si vais con prisa, o el brisket entero para compartir. Las costillas ahumadas nunca fallan',
   d='🕐 L–V 12:00–15:00 y 17:30–23:00 · S 12:00–23:00 · D 12:00–21:00 · 💷 unas 30–40 £ por persona · reservan, pero guardan mesas para quien llega sin reserva'),
 dict(z='este', n='Smoking Goat', s=['amigo'],
   dir='64 Shoreditch High Street, E1 6JJ',
   geo='Smoking Goat, 64 Shoreditch High Street, London',
   t='Tailandés del norte, de la comida que allí se pide para acompañar la bebida: picante, ahumado '
     'y para compartir. Cocina sobre brasa, carta corta que cambia y música alta. Nada que ver con '
     'el pad thai de siempre, y por eso merece la pena.',
   p='La <b>chuleta de cerdo a la brasa</b> y una ensalada de las picantes. Avisad de que la niña come, que aquí pica en serio',
   d='🕐 L–S 12:00–23:00 · D 12:00–22:00 · 💷 unas 25–35 £ por persona · sin reserva salvo grupos: se llega y se espera'),
 dict(z='este', n='Tayyabs', s=['local','barato'],
   dir='83–89 Fieldgate Street, E1 1JU · Whitechapel, 15 min andando',
   geo='Tayyabs, 83 Fieldgate Street, London',
   t='Punyabí desde 1972 y siempre lleno de gente del barrio. Las <b>chuletillas de cordero llegan '
     'a la mesa chisporroteando</b> en su plancha. Es ruidoso, rápido y muy barato para lo que dan. '
     'Aquí es donde va a comer curry quien vive en Londres, no a los restaurantes con neones de Brick Lane.',
   p='Las <b>lamb chops</b> sí o sí, un karahi para compartir y pan naan. <b>Traeos vuestra cerveza</b>: no venden alcohol pero dejan traerlo',
   d='🕐 todos los días 12:00–23:30 · 💷 unas 20 £ por persona · reservad o id a las 18:00: a las 20:00 hay cola en la calle'),
 dict(z='este', n='Poppies Fish & Chips', s=[],
   dir='6–8 Hanbury Street, E1 6QR · junto a Brick Lane',
   geo='Poppies Fish and Chips, 6 Hanbury Street, London',
   t='Para quitarse la espina del fish and chips sin acabar en una freiduría triste. Decorado de los '
     'años cincuenta, camareras con pañuelo y el pescado frito al momento. Turístico, sí, pero está bueno.',
   p='<b>Cod and chips</b> con puré de guisantes (<i>mushy peas</i>) y vinagre de malta por encima. Es lo que hace la gente de aquí',
   d='🕐 todos los días hasta las 23:00 · 💷 unas 18–22 £ el plato de bacalao · hacen para llevar y sale más barato'),
 dict(z='este', n='E. Pellicci', s=['leyenda','local','barato'],
   dir='332 Bethnal Green Road, E2 0AG',
   geo='E Pellicci, 332 Bethnal Green Road, London',
   t='Una cafetería italiana de 1900 que sigue llevando la misma familia, con el interior de '
     'marquetería de los años cuarenta <b>protegido por patrimonio</b>: no se puede tocar ni una '
     'moldura. Sirven desayuno inglés y pasta, te tratan como si te conocieran de siempre y no cabe '
     'casi nadie. Es de las cosas más auténticas que vais a ver esta semana.',
   p='El <b>full English breakfast</b> por la mañana, o unas lasañas si es mediodía',
   d='🕐 L–S 7:00–16:00, cerrado domingos · 💷 8–12 £ · solo mesas compartidas, se hace cola en la acera'),
 dict(z='este', n='Old Spitalfields Market', s=['barato'],
   dir='Horner Square, E1 6EW',
   geo='Old Spitalfields Market, London',
   t='El mercado cubierto. En la parte de <b>The Kitchens</b> hay una docena de puestos de cocinas de '
     'medio mundo —kothu roti de Sri Lanka, fideos chinos estirados a mano, sándwiches— y mesas '
     'comunes. Es la solución cuando cada uno quiere una cosa distinta, que con niños pasa siempre.',
   p='Cada uno lo suyo y a la misma mesa. El puesto de <b>Crunch</b>, de sándwiches de brioche, es el que tiene más cola y se la merece',
   d='🕐 todos los días, en general 10:00–18:00 · 💷 8–14 £ el plato · el domingo es el día grande'),
 dict(z='este', n='Bleecker Burger', s=['amigo','barato'],
   dir='Old Spitalfields Market, Lamb Street, E1 6EA · un mostrador dentro del mercado',
   geo='Bleecker Burger, Old Spitalfields Market, London',
   t='La hamburguesa de Spitalfields, y para mucha gente <b>la mejor de Londres</b>. La montó una '
     'abogada de Nueva York que dejó el despacho, se compró una furgoneta en 2012 y acabó plantando '
     'un mostrador en el mercado. No hay carta larga ni florituras: carne buena, pan y poco más, '
     'servido por una ventanilla. La <i>Bleecker Black</i>, con salsa de queso azul, es la famosa.',
   p='La <b>cheeseburger doble</b> si queréis lo clásico, o la <b>Bleecker Black</b> si os gusta el queso azul. Y las <i>angry fries</i> para compartir',
   d='🕐 desde las 11:30 hasta la noche, todos los días · 💷 10–15 £ por persona · se come de pie en el mercado o en las mesas comunes'),
 dict(z='este', n='Dishoom Shoreditch', s=[],
   dir='7 Boundary Street, E2 7JE',
   geo='Dishoom Shoreditch, 7 Boundary Street, London',
   t='Recrea los viejos cafés iraníes de Bombay y lo hace muy bien: ventiladores, mármol y retratos '
     'en las paredes. Es una cadena y está lleno de turistas, pero se come bien y no es caro. El '
     'desayuno es lo mejor que tienen.',
   p='El <b>bacon naan roll</b> del desayuno y el <b>black daal</b>, que llevan cociendo 24 horas',
   d='🕐 desde las 8:00 entre semana · 💷 20–25 £ por persona · no reservan mesas pequeñas a la hora punta: id pronto o dad el móvil y esperad en un bar'),
 dict(z='este', n='The Marksman', s=[],
   dir='254 Hackney Road, E2 7SJ',
   geo='The Marksman, 254 Hackney Road, London',
   t='Un pub de barrio con la cocina muy por encima de lo que aparenta. Vais si os coincide un '
     '<b>domingo</b>: el <i>Sunday roast</i> —asado, patatas al horno y una torta de Yorkshire del '
     'tamaño de un plato— es una comida de domingo inglesa como debe ser.',
   p='El <b>roast</b> del domingo. Y el bollo de ternera y anchoa si está en la carta',
   d='🕐 el roast solo domingos y hasta que se acaba (sobre las 16:00) · 💷 25–30 £ · <b>reservad</b> para el domingo'),
# ------------------------------------------------------------ KING'S CROSS
 dict(z='kingscross', n='Dishoom King’s Cross', s=[],
   dir='5 Stable Street, N1C 4AB · en Coal Drops Yard',
   geo='Dishoom Kings Cross, 5 Stable Street, London',
   t='El mismo de Shoreditch pero en un almacén ferroviario de tres plantas, que es el más bonito de '
     'todos. Si desayunáis aquí a las 8:30 entráis sin cola y de paso veis el edificio.',
   p='<b>Bacon naan roll</b> y un chai. Y pedid que os enseñen la planta de arriba',
   d='🕐 desayunos desde las 8:00 · 💷 20–25 £ · a mediodía y por la noche hay espera larga'),
 dict(z='kingscross', n='The Lighterman', s=[],
   dir='3 Granary Square, N1C 4BH',
   geo='The Lighterman, Granary Square, London',
   t='Un ventanal enorme sobre el canal y una terraza escalonada mirando a las fuentes. La comida es '
     'de pub correcto, sin más, pero <b>la niña puede estar jugando en las fuentes mientras vosotros '
     'os tomáis algo sentados</b> viéndola. Por eso está aquí.',
   p='Algo de picar y una caña en la terraza de arriba, que es la que ve la plaza entera',
   d='🕐 todos los días · 💷 15–25 £ · en cuanto sale el sol no hay una mesa libre fuera'),
 dict(z='kingscross', n='Roti King', s=['local','barato'],
   dir='40 Doric Way, NW1 1LH · en el sótano, junto a Euston',
   geo='Roti King, 40 Doric Way, London',
   t='Un sótano sin ninguna gracia donde se come <b>roti canai</b> malayo por seis o siete libras: '
     'una torta hojaldrada que estiran a mano y golpean contra la plancha, con un cuenco de curry '
     'para mojar. Cola en la escalera casi siempre. De lo más barato y lo más bueno de Londres.',
   p='<b>Roti canai</b> para mojar y un <i>nasi lemak</i> si tenéis hambre de verdad',
   d='🕐 12:00–15:00 y 17:30–22:00 · 💷 7–12 £ por persona · no reservan y no aceptan grupos grandes'),
 dict(z='kingscross', n='Casa Pastor y los puestos de Coal Drops Yard', s=[],
   dir='Coal Drops Yard, N1C 4DQ',
   geo='Coal Drops Yard, London',
   t='En los antiguos muelles del carbón hay una fila de sitios de comer con terraza. Casa Pastor '
     'hace tacos al pastor de trompo. Es la parada natural cuando se acaba el paseo por las plazas '
     'de King’s Cross.',
   p='Tacos al pastor, y de postre un helado en la misma plaza',
   d='🕐 todo el día · 💷 15–25 £ · hay mesas fuera y sitio para que los niños corran'),
# ------------------------------------------------------------------- SOHO
 dict(z='soho', n='Japan Centre', s=['barato','amigo'],
   dir='35b Panton Street, SW1Y 4EA · entre Piccadilly Circus y Leicester Square',
   geo='Japan Centre, 35b Panton Street, London',
   t='Supermercado japonés con barra de comida hecha al momento y, sobre todo, <b>unas neveras de '
     'sushi, bentos, ensaladas de algas y arroz que a última hora del día se rebajan a la mitad</b>. '
     'Es la mejor cena barata del centro de Londres, y sale por lo que cuesta un bocadillo.',
   p='Presentarse <b>a partir de las 20:00</b> y coger lo que tenga la pegatina roja: sushi, katsu curry, gyozas y ensalada de wakame. Se cena en un banco de Trafalgar o en el hotel',
   d='🕐 tienda L–S 10:00–21:30, D 11:00–20:00 · 🔻 <b>las rebajas del 50 % empiezan alrededor de las 20:00</b>, cuando queda hora y media para cerrar; <b>el domingo, sobre las 18:30</b>, porque cierran antes. Cuanto más tarde, más barato y menos queda'),
 dict(z='soho', n='Bao Soho', s=[],
   dir='53 Lexington Street, W1F 9AS',
   geo='Bao Soho, 53 Lexington Street, London',
   t='Once taburetes y una carta de cuatro cosas: bollos taiwaneses al vapor, blancos y esponjosos, '
     'rellenos de panceta guisada. Se come en veinte minutos y se sale contento.',
   p='El <b>classic bao</b> de cerdo y el de <i>fried chicken</i>. Uno por barba y otro más de propina',
   d='🕐 mediodía y noche · 💷 12–18 £ · no reservan: se apunta uno en la lista de la puerta'),
 dict(z='soho', n='Dumplings’ Legend', s=['barato'],
   dir='15–16 Gerrard Street, W1D 6JE · en Chinatown',
   geo='Dumplings Legend, 15 Gerrard Street, London',
   t='En plena calle de los faroles rojos, con los cocineros plegando empanadillas detrás de un '
     'cristal a la vista de todos. Los <b>xiao long bao</b> —las que llevan sopa dentro— son el '
     'motivo para entrar, y a los niños les encanta ver cómo las hacen.',
   p='<b>Xiao long bao</b> de cerdo. Se muerde un poquito por arriba, se sorbe el caldo y luego se come. Explicádselo a la niña o se quema',
   d='🕐 todos los días hasta tarde · 💷 15–20 £ por persona · las cestas son para compartir'),
 dict(z='soho', n='Flat Iron', s=['barato'],
   dir='17–18 Henrietta Street, WC2E 8QH (Covent Garden) y varios más',
   geo='Flat Iron, 17 Henrietta Street, London',
   t='Una sola cosa en la carta: un filete de <i>flat iron</i> con ensalada por un precio fijo de '
     'algo más de quince libras. Al final te traen un cucurucho de helado gratis. Es la forma más '
     'barata de cenar carne decente en el centro.',
   p='El filete, <i>medium rare</i>, y unas patatas fritas con grasa de vaca para compartir',
   d='🕐 todos los días · 💷 unas 15–20 £ por persona · no reservan, se apunta uno y te avisan al móvil'),
 dict(z='soho', n='Bar Italia', s=['leyenda'],
   dir='22 Frith Street, W1D 4RF',
   geo='Bar Italia, 22 Frith Street, London',
   t='Abierto desde 1949 y casi siempre. Barra de mármol, cafetera de las de verdad y las paredes '
     'llenas de fotos de boxeadores italianos. Es el sitio para un café de pie a las once de la noche.',
   p='Un <b>espresso</b> en la barra. Ojo, aquí el café sí se parece al de casa',
   d='🕐 hasta la madrugada · 💷 3–5 £ · en la acera, viendo pasar el Soho'),
 dict(z='soho', n='Regency Cafe', s=['leyenda','local','barato'],
   dir='17–19 Regency Street, SW1P 4BY · Westminster',
   geo='Regency Cafe, 17 Regency Street, London',
   t='Una <i>caff</i> de 1946 con la fachada negra de azulejo art déco y el interior tal cual lo '
     'dejaron. Te sientas, gritan tu pedido desde la cocina y te traen el desayuno inglés completo '
     'por menos de diez libras. Sale en cien películas. Está cerca de Westminster, así que va bien '
     'la mañana que veáis el Parlamento.',
   p='<b>Full English breakfast</b> con tostada y té. Se pide en la barra y se paga en efectivo',
   d='🕐 L–V 7:00–14:30 y 16:00–19:15, S 7:00–12:00, cerrado domingos · 💷 menos de 10 £ · <b>llevad efectivo</b>'),
# -------------------------------------------------------------------- SUR
 dict(z='sur', n='Borough Market', s=['barato'],
   dir='8 Southwark Street, SE1 1TL · bajo las vías de London Bridge',
   geo='Borough Market, London',
   t='El mercado de comida de Londres, con casi mil años de historia en el mismo sitio. Se viene a '
     'picar de puesto en puesto: queso, ostras, empanadas, chocolate. Es el mejor sitio de la ciudad '
     'para comer sin sentarse y a la niña le va a encantar porque todo el mundo da a probar.',
   p='El <b>grilled cheese de Kappacasein</b> (pan de masa madre y queso fundido de su propia lechería, en Stoney Street) y un <b>donut de Bread Ahead</b> relleno de crema, que lo hacen delante de vosotros',
   d='🕐 mercado completo M–S 10:00–17:00, algunos puestos también domingo · 💷 se come por 10–15 £ · <b>id antes de las 12</b> o no se anda'),
 dict(z='sur', n='Padella', s=['barato'],
   dir='6 Southwark Street, SE1 1TQ · en la esquina del mercado',
   geo='Padella, 6 Southwark Street, London',
   t='Pasta hecha a mano delante de vosotros, platos pequeños, entre seis y doce libras cada uno. '
     'Es probablemente la mejor relación entre lo que cuesta y lo que se come de todo Londres, y por '
     'eso hay cola desde que abren.',
   p='Los <b>pici cacio e pepe</b> y los ravioli de cordero. Dos platos por persona y pan',
   d='🕐 12:00–15:45 y 17:00–22:00 · 💷 15–20 £ por persona · <b>no reservan</b>: se apunta uno en la lista por el móvil y te avisan; id a las 17:00 y esperáis poco'),
 dict(z='sur', n='Maltby Street Market', s=['barato'],
   dir='Ropewalk, SE1 3PA · a 10 min andando de Borough',
   geo='Maltby Street Market, Ropewalk, London',
   t='Un callejón entre arcos de ferrocarril con veinte puestos y ninguna tienda de recuerdos. Es lo '
     'que era Borough antes de salir en las guías: más pequeño, más barato y con gente del barrio. '
     'Solo abre el fin de semana.',
   p='El <b>Scotch egg</b> del puesto de Finest Fayre y unos <i>waffles</i> para la niña',
   d='🕐 <b>solo sábados y domingos</b>, 10:00–17:00 · 💷 8–14 £ · mesas altas de pie, se come en el callejón'),
 dict(z='sur', n='The George Inn', s=['leyenda'],
   dir='75–77 Borough High Street, SE1 1NH',
   geo='The George Inn, Borough High Street, London',
   t='El <b>último pub de Londres con galería de madera</b>, de 1677, escondido en un patio y '
     'propiedad del National Trust. Dickens lo menciona en <i>La pequeña Dorrit</i>. Se entra a '
     'tomar una pinta en el patio y a mirar hacia arriba.',
   p='Una pinta de <i>bitter</i> —la cerveza inglesa de verdad, poco fría y poco gaseosa— en el patio',
   d='🕐 todos los días · 💷 6–7 £ la pinta · se pide en la barra y se paga en el momento: aquí nadie viene a tomar nota'),
# ----------------------------------------------------------------- MUSEOS
 dict(z='museos', n='Las Refreshment Rooms del V&A', s=['leyenda','barato'],
   dir='Victoria and Albert Museum, Cromwell Road, SW7 2RL',
   geo='Victoria and Albert Museum, Cromwell Road, London',
   t='La <b>primera cafetería de museo del mundo</b>, de 1868, con tres salas decoradas por William '
     'Morris y Edward Poynter: azulejos, vidrieras y columnas. Se paga como una cafetería normal y '
     'se está sentado en una obra de arte. Entrar al museo es gratis, así que se puede venir solo a esto.',
   p='Un té con un trozo de tarta en la <b>Gamble Room</b>, la de las columnas de cerámica',
   d='🕐 con el museo, 10:00–17:45 · 💷 6–12 £ · en el patio de fuera hay una lámina de agua donde los niños se meten en verano'),
 dict(z='museos', n='Japan House', s=[],
   dir='101–111 Kensington High Street, W8 5SA',
   geo='Japan House London, 101 Kensington High Street, London',
   t='La casa de la cultura japonesa en Londres, y <b>entrar es gratis</b>: tres plantas con una '
     'exposición que va cambiando, una tienda de objetos japoneses muy bien elegidos —papelería, '
     'cerámica, cuchillos—, una biblioteca y un mostrador de té. Arriba está el restaurante AKIRA, '
     'que ya es caro; abajo se puede tomar algo sin gastar.',
   p='Ver la exposición de abajo, bajar a la tienda y tomar un <i>matcha</i> en el mostrador',
   d='🕐 L–S 10:00–20:00, D 12:00–18:00 · 💷 la exposición y la tienda, gratis · metro High Street Kensington, a 100 m'),
 dict(z='museos', n='Picnic en Kensington Gardens', s=['barato'],
   dir='Comprad en el Whole Foods de Kensington High Street, W8 5SE',
   geo='Kensington Gardens, London',
   t='Alrededor de los museos casi todo es caro y regular. La jugada buena es comprar comida hecha '
     'en un supermercado y cruzar al parque: hay césped, ardillas que se acercan a la mano y el '
     '<a href="#nina">parque infantil del barco pirata</a> a diez minutos.',
   p='Sándwiches, fruta y algo de beber. En cualquier supermercado inglés hay comida preparada decente por 4–5 £',
   d='💷 15 £ los tres · si llueve, los propios museos tienen cafetería y se puede entrar comida al patio del V&A'),
# -------------------------------------------------------------- GREENWICH
 dict(z='greenwich', n='Goddards at Greenwich', s=['leyenda','barato'],
   dir='22 King William Walk, SE10 9HU',
   geo='Goddards at Greenwich, 22 King William Walk, London',
   t='Pie and mash: empanada de carne, puré de patata y una salsa verde de perejil llamada '
     '<i>liquor</i>. Es la comida obrera de Londres desde el siglo XIX y esta familia lleva '
     'haciéndolo desde 1890. No es alta cocina, es historia comestible y cuesta ocho libras.',
   p='<b>Pie and mash</b> con <i>liquor</i>. Los valientes, con anguila en gelatina',
   d='🕐 todos los días 10:00–19:00 · 💷 8–12 £ · a un paso del Cutty Sark'),
 dict(z='greenwich', n='Greenwich Market', s=['barato'],
   dir='5B Greenwich Market, SE10 9HZ',
   geo='Greenwich Market, London',
   t='Mercado cubierto del siglo XIX, más pequeño y menos agobiante que los del centro, con puestos '
     'de comida de medio mundo y artesanía. Perfecto para comer el día que bajéis en barco.',
   p='Lo que os entre por los ojos, y unos <i>brownies</i> de postre',
   d='🕐 todos los días 10:00–17:30 · 💷 8–14 £ · techado, así que sirve también si llueve'),
 dict(z='greenwich', n='The Trafalgar Tavern', s=['leyenda'],
   dir='Park Row, SE10 9NW · junto al río',
   geo='Trafalgar Tavern, Park Row, London',
   t='Pub de 1837 con los ventanales dando al Támesis, donde los ministros victorianos venían a '
     'comer <i>whitebait</i> —pescaditos fritos— del río. Se toma algo mirando el agua y Canary '
     'Wharf enfrente.',
   p='Una pinta con vistas, o el <i>fish and chips</i> si es la hora',
   d='🕐 todos los días · 💷 6–7 £ la pinta, 20 £ comer · dos minutos andando desde el parque'),
]
