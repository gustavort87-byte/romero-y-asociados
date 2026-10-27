#!/usr/bin/env bash
# Publica site/ en GitHub Pages a través de la rama gh-pages.
# La copia publicada lleva noindex (scripts/noindex.py); site/ en main sigue siendo el clon fiel.
# Uso, desde la raíz del repo: bash scripts/publicar.sh
set -euo pipefail
cd "$(dirname "$0")/.."
tmp="$(mktemp -d)"
trap 'git worktree remove --force "$tmp" 2>/dev/null || true' EXIT
git fetch -q origin gh-pages 2>/dev/null || true
if git show-ref -q --verify refs/remotes/origin/gh-pages; then
  git worktree add -q -B gh-pages "$tmp" origin/gh-pages
else
  git worktree add -q --detach "$tmp"
  git -C "$tmp" checkout -q --orphan gh-pages
fi
git -C "$tmp" rm -q -rf --ignore-unmatch .
cp -r site/. "$tmp/"
touch "$tmp/.nojekyll"
printf '* -text\n' > "$tmp/.gitattributes"
python "$(pwd)/scripts/noindex.py" "$tmp/index.html"
git -C "$tmp" add -A
if git -C "$tmp" diff --cached --quiet; then echo "Sin cambios que publicar."; exit 0; fi
git -C "$tmp" commit -q -m "Publicar site/ ($(git rev-parse --short HEAD))"
git -C "$tmp" push -q origin gh-pages
echo "Publicado: https://gustavort87-byte.github.io/romero-y-asociados/"
