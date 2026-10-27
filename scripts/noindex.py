"""Añade <meta name="robots" content="noindex"> a la copia publicada en GitHub Pages.

Solo corre en el deploy: site/ en el repo sigue siendo el clon fiel, listo para el hosting real.
index.html es un bundle de Claude Design: la plantilla (JSON) reemplaza el <head> al cargar,
así que la etiqueta va en el cargador y también dentro de la plantilla.
"""
import json, pathlib, re, sys

BS = chr(92)
META = '<meta name="robots" content="noindex, nofollow">'

def esc(text):
    return json.dumps(text, ensure_ascii=False)[1:-1].replace('</', '<' + BS + 'u002F')

def main(path):
    p = pathlib.Path(path)
    s = p.read_text(encoding='utf-8')
    if 'name="robots"' in s:
        return
    loader = '  <meta charset="utf-8">\n'
    assert s.count(loader) == 1, 'cargador sin <meta charset>'
    s = s.replace(loader, loader + '  ' + META + '\n')
    anchor = esc('<meta name="viewport" content="width=device-width, initial-scale=1">')
    assert s.count(anchor) == 1, 'plantilla sin meta viewport'
    s = s.replace(anchor, anchor + BS + 'n' + esc(META))
    tpl = json.loads(re.search(r'<script type="__bundler/template">(.*?)</script>', s, re.S).group(1))
    assert META in tpl
    p.write_text(s, encoding='utf-8', newline='')

if __name__ == '__main__':
    main(sys.argv[1])
