# Romero y Asociados

Proyecto: extracción completa y clon exacto de https://romeroabogados.com.mx/ (Romero y Asociados · Abogados, despacho en San Luis Potosí, México). Es un sitio de una sola página.

Captura: 2026-10-26. El contenido se obtuvo con Firecrawl (1 crédito, `maxAge: 0`, en vivo) y el HTML se descargó byte a byte del servidor para hacer el clon.

## Cómo ver el clon

El clon está en `site/`. Funciona de las dos formas:

- **Doble clic en `site/index.html`:** se ve igual que el sitio. Todas las fuentes e imágenes van dentro del HTML. Solo el mapa de Google necesita internet.
- **Con servidor:** `cd site` y luego `python -m http.server 8000`, y abrir http://localhost:8000/.

Para publicarlo, sube el contenido de `site/` tal cual a la raíz de cualquier hosting estático.

## Publicado en GitHub Pages

- Repo: https://github.com/gustavort87-byte/romero-y-asociados
- Sitio: https://gustavort87-byte.github.io/romero-y-asociados/
- Página puente: https://gustavort87-byte.github.io/romero-y-asociados/alianza-integraterra.html

El sitio se sirve desde la rama `gh-pages`, que contiene solo `site/` con `noindex, nofollow` para que Google no la muestre ni compita con romeroabogados.com.mx. Para volver a publicar después de cambiar `site/`, ejecuta desde la raíz del repo: `bash scripts/publicar.sh`. La etiqueta se inyecta solo en esa rama (`scripts/noindex.py`), así que `site/` en `main` sigue siendo el clon fiel, listo para el hosting real.

## Cómo está hecho el sitio original

Es un export "bundle" de Claude Design: un único `index.html` de 4.9 MB que trae dentro, en base64, 25 recursos. Al cargar, un script los desempaqueta como `blob:` y reemplaza la página por la plantilla real. Por eso Firecrawl ve las imágenes como `blob:https://…`.

- **Recursos dentro del bundle:** logo (PNG 2000×2000), fondo del hero (PNG 1920×1080), 20 archivos de fuente woff2 (Playfair Display, Cormorant Garamond, Lato), el runtime de plantillas de Claude Design (`dc-runtime.js`), y React 18.3.1 y ReactDOM, que vienen incluidos pero la página no usa.
- **Único recurso externo:** el iframe de Google Maps.
- **En el servidor** solo hay `/` (HTML), `/og-logo.png` y `/robots.txt` (el que Cloudflare pone por defecto). No hay favicon, sitemap ni manifest: esas rutas dan 404. `/index.html` redirige a `/`.

## Alianza Romero y Asociados → Integra Terra (2026-10-27)

Es el camino inverso al de `Integraterra/site/alianza-romero-abogados.html`. La página puente es `site/alianza-integraterra.html`.

**Cómo se llega:** la tarjeta **VI · Derecho Agrario y de Tierras** de `site/index.html` tiene ahora un enlace, "Gestión territorial con Integra Terra →", con los mismos estilos de la tarjeta (Lato 13 px en mayúsculas, dorado `#D6B26E` que pasa a blanco en hover). Abre la página puente en una pestaña nueva con `?servicio=tierra`. Es el único cambio visible en `index.html`. La fila de las tarjetas V a VIII crece lo que ocupa ese enlace.

**Qué hace la página:**
- Explica que Romero y Asociados e Integra Terra son socios y muestra los logos de las dos marcas.
- Presenta los 4 servicios de Integra Terra con su texto y la lista de sus 8 sectores.
- Muestra una cuenta regresiva de 12 segundos y luego lleva a integraterra.com. El cliente puede pulsar "Ir ahora" o "Quedarme a leer", que detiene la redirección. La cuenta se pausa si la pestaña está en segundo plano.
- Cada tarjeta de servicio lleva a la sección `#servicios` de Integra Terra.
- Tiene un botón de WhatsApp de Integra Terra (444 194 4775) con el mensaje "Hola, vengo de Romero y Asociados y me gustaría conocer sus servicios."
- El footer tiene dos columnas de contacto: Romero y Asociados e Integra Terra.
- Lleva `noindex`, para que Google no la muestre como página propia.

**Diseño:** la estructura usa la identidad de Romero: el header del sitio, el hero con su fondo de ciudad nocturna, Lato y Playfair Display, azul `#16233F` y dorado `#B08D45`. Los bloques de Integra Terra usan la suya: Archivo 800, azul `#23345a`, café `#7a4a26`, beige `#ECE6DC` y esquinas rectas, con su logo SVG original. Las fuentes son locales (`site/fonts/fonts.css`), copiadas del bundle de Romero y del clon de Integraterra, así que la página se ve igual sin internet.

**Parámetros de URL:**

| URL | Efecto |
|---|---|
| `alianza-integraterra.html` | Página general; redirige a la home de Integra Terra |
| `…?servicio=tierra` | Resalta el servicio, añade "Para tu consulta de … te atenderá su equipo especializado." y redirige a `#servicios`. Valores: `tierra`, `social`, `ambiental`, `proyectos` |
| `…?segundos=20` | Cambia la espera. `segundos=0` desactiva la redirección automática |

Todos los enlaces hacia Integra Terra llevan `utm_source=romeroabogados&utm_medium=referral&utm_campaign=alianza`, más `utm_content=<servicio>` en las tarjetas. Así Integra Terra puede medir en su analítica cuántos clientes llegan desde Romero.

**Verificado (Chrome headless), con doble clic y con servidor:**
- Clic en el enlace de la tarjeta VI → se abre la pestaña nueva con "Tierra" resaltado → a los 12 s redirige a `integraterra.com/?utm_…&utm_content=tierra#servicios`.
- "Quedarme a leer" detiene la redirección; `?segundos=0` también.
- Las 4 fuentes cargan (Lato, Playfair Display, Archivo, Cormorant Garamond).
- No hay scroll horizontal a 1440, 768 y 390 px, y el header cabe desde 320 px.
- Sin errores de consola.

## Verificación del clon (2026-10-26, antes de añadir el enlace de la alianza)

Comparado contra el sitio en vivo con Chrome headless (Playwright), con el clon abierto por doble clic (`file://`) y por servidor (`http://`):

| Prueba | Resultado |
|---|---|
| Página completa a 1920 / 1440 / 1024 / 768 / 375 px | 0 píxeles distintos, mismo alto, en los dos modos |
| Página completa en iPhone SE, iPhone 14 Pro Max, Pixel 7 y iPad Mini (con su escala de pantalla) | 0 píxeles distintos en los dos modos |
| Posición, tamaño, fuente, peso, interlineado, color, fondo y espaciado de los 188 elementos, en los 9 tamaños | 0 diferencias |
| Los 14 enlaces (5 de WhatsApp, teléfono, correo, Maps, 6 anclas): texto, destino y `target` | Idénticos |
| Hover de los 14 enlaces y header fijo al hacer scroll | Idénticos |
| Mapa de Google | Carga en los tres modos, también con doble clic. Mismo mapa; solo hay diferencias de antialiasing que Google introduce entre una carga y otra |
| Versión desempaquetada (`unpacked/index.html`) a 1440 y 375 px | 0 píxeles distintos |
| Errores de consola | Ninguno, ni en vivo ni en el clon |

## Estructura

```
Romero-y-Asociados/
├── site/                     ← CLON FUNCIONAL (lo que se publica)
│   ├── index.html            HTML original + favicon + enlace de la alianza (ver "Cambios")
│   ├── alianza-integraterra.html  Página puente hacia Integra Terra
│   ├── fonts/                Lato, Playfair, Cormorant y Archivo locales + fonts.css (para la página puente)
│   ├── img/                  hero-fondo.jpg y logos de Integra Terra (para la página puente)
│   ├── og-logo.png           Imagen para compartir en redes (original, 1200×630)
│   ├── favicon.ico           Logo en 16, 32, 48 y 64 px (nuevo)
│   ├── icon-192.png, icon-512.png, apple-touch-icon.png   (nuevos, del logo)
├── unpacked/                 ← CÓDIGO FUENTE desempaquetado (para editar)
│   ├── index.html            La plantilla real con rutas a archivos sueltos (se ve igual)
│   ├── template.html         La plantilla tal como viene en el bundle (rutas = UUID)
│   ├── manifest-map.json     Qué UUID corresponde a cada archivo
│   ├── img/                  logo-romero.png, hero-fondo.png
│   ├── fonts/                20 woff2
│   └── js/                   dc-runtime.js, react, react-dom
├── assets/                   Logo, fondo del hero, og-image e íconos con nombres legibles
├── contenido.md              Todo el texto del sitio por secciones, más metadatos
├── datos.json                Contacto, áreas de práctica, valores, enlaces (estructurado)
├── branding.json             Colores, tipografía, botones, layout
├── raw/
│   ├── index.original.html   HTML exactamente como lo sirve el servidor (sin tocar)
│   ├── headers.txt, robots.txt, og-logo.png
├── ref/                      Copia anterior (idéntica byte a byte a raw/)
└── screenshots/live-*.png    Capturas de referencia del sitio en vivo (9 tamaños)
```

## Cambios frente al original

`site/index.html` es igual a `raw/index.original.html` salvo estos tres cambios:

1. **Favicon:** el sitio original no tiene, y el navegador muestra el ícono genérico. Se añadieron tres etiquetas `<link rel="icon">` / `apple-touch-icon`, tanto en el cargador como dentro de la plantilla, porque la plantilla reemplaza el `<head>`. Apuntan a íconos recortados del hexágono con la "R" del logo original. No cambia nada de la página: la comparación de píxeles dio 0.
2. **Enlace de la alianza** en la tarjeta VI (ver la sección "Alianza"). Se insertó en la plantilla JSON del bundle, donde `</` va escapado como `</`, y también en `unpacked/index.html`.
3. **Fondo aurora en el hero (2026-10-27):** bandas de luz azul que se mueven despacio desde la esquina superior derecha, encima de la foto de la ciudad. Es la versión en CSS puro del componente React `AuroraBackground` (shadcn/Tailwind). El sitio es HTML estático sin React ni Tailwind, así que se portó la misma técnica: dos `repeating-linear-gradient`, `blur(10px)`, `mix-blend-mode: difference`, animación de 60 s y máscara radial. En lugar de la paleta de Tailwind usa los azules del sitio (`#16233F` como velo y `#3A5A9C`, `#5B79B8`, `#2F4C86`, `#B9C1D4`, `#C6CDDD` en las bandas). Con "reducir movimiento" activado queda fija. Son las reglas `#inicio .ra-aurora` del `<style>` y un `<div class="ra-aurora">` dentro del `<header id="inicio">`.

Si se quiere el original sin ningún cambio, basta con usar `raw/index.original.html` renombrado a `index.html`.

## Para editar el sitio

Lo más cómodo es trabajar sobre `unpacked/index.html`: los textos están en HTML legible y las imágenes y fuentes son archivos normales. Funciona con doble clic y con servidor. Los valores de WhatsApp (teléfono `+524445393428` y mensaje) están en el script `text/x-dc` al final del archivo.

## Notas sobre el sitio original

- **Teléfonos:** se muestran "444 493 3400 · 444 791 9737", pero el enlace `tel:` solo marca el primero.
- **Equipo:** la sección no tiene nombres ni fotos, solo tres círculos decorativos.
- **Áreas:** el sitio tiene 8 áreas de práctica. La página puente de Integraterra ya las lista todas (la VI, Agrario, se añadió el 2026-10-27).
- **robots.txt:** es el que Cloudflare pone por defecto: `Allow: /` con `Content-Signal: search=yes, ai-train=no, use=reference` y bloqueo de crawlers de entrenamiento. Esta copia se hizo para el cliente; no es entrenamiento.
- **Contacto:** WhatsApp 444 539 3428, tel. 444 493 3400 y 444 791 9737, romeroabogadosadmin@gmail.com, Cordillera Real #316, Col. Lomas 3ª Sección, C.P. 78210, San Luis Potosí. Todos los CTA abren WhatsApp y no hay formulario.
