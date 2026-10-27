# Romero y Asociados

Proyecto: extracción completa y clon exacto de https://romeroabogados.com.mx/ (Romero y Asociados · Abogados, despacho en San Luis Potosí, México). Es un sitio de una sola página.

Captura: 2026-10-26. El contenido se obtuvo con Firecrawl (1 crédito, `maxAge: 0`, en vivo) y el HTML se descargó byte a byte del servidor para hacer el clon.

## Cómo ver el sitio

El sitio está en `site/`. Desde el 2026-10-27 `site/index.html` es la **versión optimizada**: HTML estático ya renderizado, de 40 KB (ver "Rendimiento"). Funciona de las dos formas:

- **Doble clic en `site/index.html`:** se ve igual que el sitio. Las fuentes y las imágenes son archivos locales en `site/fonts/` y `site/img/`. Solo el mapa de Google necesita internet.
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

## Rendimiento (PageSpeed / Lighthouse, 2026-10-27)

El bundle original tardaba ~19 s en mostrar algo en un móvil. Primero había que descargar 4.9 MB de HTML. Después el navegador decodificaba el base64, descomprimía los scripts y armaba la página con JavaScript. PageSpeed le daba 47 en Rendimiento al sitio real, con FCP y LCP de 18.7 s.

`scripts/build_static.py` renderiza el bundle una vez con Chromium y guarda el resultado como `site/index.html`:

- **HTML estático ya armado, sin JavaScript:** 40 KB en lugar de 4.9 MB. Las reglas de hover que el motor generaba en tiempo de ejecución (`.scp0` … `.scp6`) se copian al `<style>`.
- **Imágenes en WebP del tamaño mostrado:**
  - el fondo del hero pasa de PNG de 2 MB a `img/hero-fondo.webp`, de 15 KB;
  - el logo pasa de PNG de 2000 px y 1.1 MB a `img/logo-romero-{190,380,570}.webp` con `srcset`, de 5 a 15 KB.
- **Fuentes como archivos** (`fonts/`, solo latin y latin-ext) en lugar de base64 dentro del HTML. Se precargan Playfair y Lato, pero solo por http(s), porque con doble clic Chrome bloquea la precarga.
- **`lang="es"`** en `<html>` (lo pedía Accesibilidad).
- **React, ReactDOM y el motor de plantillas** ya no se cargan; la página no los necesitaba.

Lighthouse en móvil (Moto G Power, 4G lento simulado), con las dos versiones servidas igual en local:

| | Rendimiento | Accesibilidad | Prácticas | SEO | FCP | LCP | TBT | Peso |
|---|---|---|---|---|---|---|---|---|
| Bundle | 26 | 89 | 100 | 100 | 25.0 s | 27.2 s | 3,220 ms | 4.8 MB |
| Estático | **99** | **95** | 100 | 100 | **1.2 s** | **2.1 s** | **0 ms** | **195 KB** |

En Accesibilidad solo queda el contraste de los 3 botones "Agendar cita": texto blanco sobre dorado `#B08D45`, 3.1:1 cuando el mínimo es 4.5:1. El cliente decidió conservar los colores de marca. Las opciones que pasan son texto azul marino `#16233F` sobre el mismo dorado (5.0:1) o un dorado más oscuro `#8F6F30` con texto blanco (4.7:1).

**Se ve igual que el bundle:** comparado en 10 tamaños, a 1920, 1440, 1024, 768 y 375 px y en iPhone SE, iPhone 14 Pro Max, Pixel 7, iPad Mini y Moto G4, con doble clic y con servidor:
- Posición, tamaño, fuente, color y espaciado de los 158 elementos: 0 diferencias.
- Los 14 enlaces: idénticos.
- Hover de 23 elementos: idéntico.
- Píxeles: solo cambian dentro del hero, por la recompresión de las imágenes. Casi todas las diferencias son de 1 a 16 niveles sobre 255. Las mayores están en el borde de las letras del logo, que ahora se ve un poco más nítido.
- Sin errores de consola.

**El sitio real** (romeroabogados.com.mx) seguirá con la nota baja hasta que se suba allí el contenido de `site/`. Su `robots.txt`, que gestiona Cloudflare, también resta en SEO porque Lighthouse no reconoce la directiva `Content-Signal`. Eso se ajusta en el panel de Cloudflare, no en los archivos del sitio.

**Para volver a generar** `site/index.html`, por ejemplo después de editar el bundle, se ejecuta `python scripts/build_static.py`. La fuente es `raw/index.bundle.html`, el bundle con favicon y enlace a Integra Terra. También se puede editar `site/index.html` directamente: ahora es HTML normal.

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
│   ├── index.html            Versión estática optimizada (generada por scripts/build_static.py)
│   ├── alianza-integraterra.html  Página puente hacia Integra Terra
│   ├── fonts/                Lato, Playfair, Cormorant y Archivo locales + fonts.css (para la página puente)
│   ├── img/                  hero-fondo.webp, logo-romero-*.webp; hero-fondo.jpg y logos de Integra Terra (página puente)
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
│   ├── index.bundle.html     El bundle con favicon + enlace de la alianza (fuente de build_static.py)
│   ├── headers.txt, robots.txt, og-logo.png
├── ref/                      Copia anterior (idéntica byte a byte a raw/)
└── screenshots/live-*.png    Capturas de referencia del sitio en vivo (9 tamaños)
```

## Cambios frente al original

`raw/index.bundle.html` (de donde sale `site/index.html`) es igual a `raw/index.original.html` salvo estos dos cambios. Además, `site/index.html` lleva la optimización descrita en "Rendimiento" y `lang="es"`.

1. **Favicon:** el sitio original no tiene, y el navegador muestra el ícono genérico. Se añadieron tres etiquetas `<link rel="icon">` / `apple-touch-icon`, tanto en el cargador como dentro de la plantilla, porque la plantilla reemplaza el `<head>`. Apuntan a íconos recortados del hexágono con la "R" del logo original. No cambia nada de la página: la comparación de píxeles dio 0.
2. **Enlace de la alianza** en la tarjeta VI (ver la sección "Alianza"). Se insertó en la plantilla JSON del bundle, donde `</` va escapado como `<\u002F`, y también en `unpacked/index.html`.

Si se quiere el original sin ningún cambio, basta con usar `raw/index.original.html` renombrado a `index.html`.

## Para editar el sitio

Lo más directo es editar `site/index.html`, que ahora es HTML normal sin motor de plantillas. Los enlaces de WhatsApp ya están escritos completos en cada botón. Si se edita el bundle (`raw/index.bundle.html`, o su versión legible `unpacked/index.html`), hay que volver a generar el sitio con `python scripts/build_static.py`.

## Notas sobre el sitio original

- **Teléfonos:** se muestran "444 493 3400 · 444 791 9737", pero el enlace `tel:` solo marca el primero.
- **Equipo:** la sección no tiene nombres ni fotos, solo tres círculos decorativos.
- **Áreas:** el sitio tiene 8 áreas de práctica. La página puente de Integraterra ya las lista todas (la VI, Agrario, se añadió el 2026-10-27).
- **robots.txt:** es el que Cloudflare pone por defecto: `Allow: /` con `Content-Signal: search=yes, ai-train=no, use=reference` y bloqueo de crawlers de entrenamiento. Esta copia se hizo para el cliente; no es entrenamiento.
- **Contacto:** WhatsApp 444 539 3428, tel. 444 493 3400 y 444 791 9737, romeroabogadosadmin@gmail.com, Cordillera Real #316, Col. Lomas 3ª Sección, C.P. 78210, San Luis Potosí. Todos los CTA abren WhatsApp y no hay formulario.


## Publicado en Cloudflare Workers (2026-10-27)

El Worker `shiny-sun-4a36` de la cuenta de Cloudflare de Romero y Asociados esta conectado a este repo (rama `main`). Cada push ejecuta `npx wrangler deploy` y publica `site/` como static assets segun `wrangler.jsonc`.
