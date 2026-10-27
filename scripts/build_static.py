"""Genera site/index.html como HTML estático y ligero a partir del bundle de Claude Design.

El bundle original (un HTML de 4.9 MB que se desempaqueta y se arma con JavaScript) tarda ~19 s
en mostrar algo en un móvil. Este script lo renderiza una vez con Chromium y guarda el resultado:

- el DOM final, ya armado, sin scripts (no hace falta JavaScript para ver la página);
- las reglas de hover que el motor genera en tiempo de ejecución (.scp0 … .scp6);
- el logo y el fondo del hero en WebP del tamaño que se muestra, en lugar de PNG de 1-2 MB;
- las fuentes como archivos woff2 (latin y latin-ext) en lugar de base64 dentro del HTML;
- lang="es" en <html>.

Uso, desde la raíz del repo:  python scripts/build_static.py
Fuente: raw/index.bundle.html (el bundle con favicon y enlace a Integra Terra).
Requiere: pip install playwright pillow  y  python -m playwright install chromium
"""
import html as htmlmod
import pathlib
import re
import shutil

from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
BUNDLE = ROOT / 'raw' / 'index.bundle.html'
SITE = ROOT / 'site'
IMG = SITE / 'img'
FONTS = SITE / 'fonts'

LATIN = ('U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, '
         'U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD')
LATIN_EXT = ('U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, U+02DD-02FF, U+0304, U+0308, U+0329, '
             'U+1D00-1DBF, U+1E00-1E9F, U+1EF2-1EFF, U+2020, U+20A0-20AB, U+20AD-20C4, U+2113, U+2C60-2C7F, U+A720-A7FF')
# familia, estilo, pesos, archivo (sin el sufijo de subconjunto)
FACES = [
    ('Lato', 'normal', '300', 'lato-300'),
    ('Lato', 'normal', '400', 'lato-400'),
    ('Lato', 'normal', '700', 'lato-700'),
    ('Playfair Display', 'normal', '500 700', 'playfair-display'),
    ('Cormorant Garamond', 'normal', '400 700', 'cormorant-garamond'),
    ('Cormorant Garamond', 'italic', '400', 'cormorant-garamond-italic'),
]


def build_images():
    IMG.mkdir(exist_ok=True)
    hero = Image.open(ROOT / 'unpacked' / 'img' / 'hero-fondo.png').convert('RGB')
    hero.save(IMG / 'hero-fondo.webp', 'WEBP', quality=88, method=6)
    logo = Image.open(ROOT / 'unpacked' / 'img' / 'logo-romero.png').convert('RGB')
    for w in (190, 380, 570):
        logo.resize((w, w), Image.LANCZOS).save(IMG / f'logo-romero-{w}.webp', 'WEBP', quality=90, method=6)


def build_fonts():
    FONTS.mkdir(exist_ok=True)
    rules = []
    for family, style, weight, stem in FACES:
        for subset, rng in (('latin', LATIN), ('latin-ext', LATIN_EXT)):
            name = f'{stem}-{subset}.woff2'
            src = ROOT / 'unpacked' / 'fonts' / name
            if not (FONTS / name).exists():
                shutil.copyfile(src, FONTS / name)
            rules.append(f"@font-face{{font-family:'{family}';font-style:{style};font-weight:{weight};"
                         f"font-display:swap;src:url(fonts/{name}) format('woff2');unicode-range:{rng}}}")
    return '\n'.join(rules)


def render():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': 1440, 'height': 900})
        page.goto(BUNDLE.as_uri())
        page.wait_for_function("document.body && document.body.innerText.includes('Tu tranquilidad')")
        page.wait_for_timeout(1000)
        data = page.evaluate("""() => {
            const sheets = [...document.styleSheets];
            const textOf = s => [...s.cssRules].map(r => r.cssText).join('\\n');
            // reglas de hover que el motor inserta por CSSOM (su <style> queda vacío en el HTML)
            const hover = sheets.filter(s => [...s.cssRules].some(r => /^\\.scp\\d+:hover/.test(r.selectorText || ''))).map(textOf).join('\\n');
            const layout = sheets.filter(s => [...s.cssRules].some(r => (r.selectorText || '').includes('#dc-root'))).map(textOf).join('\\n');
            const site = sheets.filter(s => [...s.cssRules].some(r => (r.selectorText || '') === '.nav-links' || (r.cssText || '').includes('.nav-links'))).map(textOf).join('\\n');
            const metas = [...document.head.querySelectorAll('meta[name], meta[property], link[rel*=icon]')].map(e => e.outerHTML);
            const root = document.getElementById('dc-root').cloneNode(true);
            root.querySelectorAll('[data-dc-tpl]').forEach(e => e.removeAttribute('data-dc-tpl'));
            root.querySelectorAll('script').forEach(e => e.remove());
            return { hover, layout, site, metas, title: document.title, body: root.outerHTML };
        }""")
        browser.close()
    return data


def main():
    if not BUNDLE.exists():
        raise SystemExit(f'Falta {BUNDLE}')
    build_images()
    fonts_css = build_fonts()
    d = render()
    body = d['body']

    imgs = re.findall(r'<img [^>]*src="blob:[^"]*"[^>]*>', body)
    assert len(imgs) == 2, f'se esperaban 2 imágenes blob, hay {len(imgs)}'
    hero_tag, logo_tag = imgs
    assert 'object-fit: cover' in hero_tag and 'width="190"' in logo_tag
    body = body.replace(hero_tag, re.sub(r'src="blob:[^"]*"',
        'src="img/hero-fondo.webp" width="1920" height="1080" fetchpriority="high" decoding="async"', hero_tag))
    body = body.replace(logo_tag, re.sub(r'src="blob:[^"]*"',
        'src="img/logo-romero-380.webp" srcset="img/logo-romero-190.webp 1x, img/logo-romero-380.webp 2x, '
        'img/logo-romero-570.webp 3x" fetchpriority="high"', logo_tag))
    assert 'blob:' not in body

    metas = [m for m in d['metas'] if 'name="viewport"' not in m]
    out = f'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{htmlmod.escape(d["title"], quote=False)}</title>
{chr(10).join(metas)}
<script>/* precarga de fuentes solo por http(s): con doble clic (file://) Chrome la bloquea por CORS */
if (location.protocol !== 'file:') ['playfair-display-latin', 'lato-400-latin'].forEach(function (f) {{
  var l = document.createElement('link'); l.rel = 'preload'; l.as = 'font'; l.type = 'font/woff2';
  l.crossOrigin = ''; l.href = 'fonts/' + f + '.woff2'; document.head.appendChild(l); }});</script>
<link rel="preload" href="img/hero-fondo.webp" as="image" type="image/webp" fetchpriority="high">
<style>
{fonts_css}
{d["layout"]}
{d["site"]}
{d["hover"]}
</style>
</head>
<body>
{body}
</body>
</html>
'''
    (SITE / 'index.html').write_text(out, encoding='utf-8', newline='\n')
    print(f'site/index.html: {len(out.encode()) // 1024} KB')


if __name__ == '__main__':
    main()
