# GUARDIAN — secuencia de identidad, 5 segundos

## Piezas realistas, revisión actual

Generadas con ImageGen integrado a partir del emblema original. Prompt de espada: aislar una espada completa, vertical, pomo arriba y punta abajo; reconstruir lo oculto por el yelmo; conservar acero envejecido rayado, guarda ancha, pomo redondo y cuero marrón; transparencia real; sin estilo vectorial, sin texto ni elementos adicionales. Prompt de yelmo: aislar únicamente el casco abierto con penacho rojo; eliminar espadas; preservar forma frontal, remaches, cuero y acero martillado, sobre transparencia.

Archivos: `demo/fraudguard/static/guardian-steel-sword.png` y `demo/fraudguard/static/guardian-helmet-layer.png`. La secuencia usa dos instancias de la espada realista y una capa de yelmo; ya no usa geometría dibujada de espada. Duración: cinco segundos; transformaciones y opacidad continuas, sin escalones de fotogramas. Objetivo de fluidez: 60 fps, dependiente de pantalla y equipo; no se afirma una medición de rendimiento.

Crear una animación cinematográfica de exactamente cinco segundos para el emblema GUARDIAN situado en la esquina superior izquierda. Mantener su identidad antigua: acero, empuñaduras de cuero, yelmo abierto y penacho rojo. Dos espadas de acero entran desde lados opuestos, aceleran y chocan en el centro. En el contacto surge un destello breve y una ráfaga radial de chispas doradas. Las espadas retroceden ligeramente por el impacto y se colocan cruzadas detrás. Desde el fondo emerge el yelmo, aumentando de tamaño y pasando del desenfoque a un acabado nítido. Terminar con el emblema original inmóvil y legible. Fondo transparente, adaptación a modo claro y oscuro. Una reproducción al entrar, sin bucle ni audio; respetar movimiento reducido.

Secuencia implementada con capas SVG y CSS: entrada 0–1,5 s; choque y chispas 1,5–2,3 s; revelado 2,3–4 s; asentamiento 4–5 s. Pulsar el emblema permite reproducirla de nuevo. La reproducción solicitada expresamente por el propietario se mantiene activa aunque el navegador anuncie movimiento reducido.
