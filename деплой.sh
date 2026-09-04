#!/usr/bin/env bash
# Пересобрать сайт и выложить его на GitHub Pages.
# Ветка gh-pages содержит только сборку — исходники живут в main.
set -euo pipefail
ЗДЕСЬ="$(cd "$(dirname "$0")" && pwd)"
РЕПО="s5hyhbpftv-alt/sunc-10l"

cd "$ЗДЕСЬ"
python3 книга.py
python3 книга-крафт.py
python3 build_v1.py
python3 экспорт.py

cp "out/Расписание 10-Л — СУНЦ МГУ.pdf" web/public/pdf/10L-chernila.pdf
cp "out/Расписание 10-Л — крафт.pdf"     web/public/pdf/10L-kraft.pdf
cp out/v1-raspisanie-10L-SUNC-MGU.pdf    web/public/pdf/10L-plakat-a3.pdf
cp assets/kraft.jpg                      web/public/kraft.jpg

cd web && npm run build && cd ..

ВРЕМЕННО="$(mktemp -d)"
cp -R web/dist/. "$ВРЕМЕННО/"
touch "$ВРЕМЕННО/.nojekyll"
cd "$ВРЕМЕННО"
git init -q && git checkout -qb gh-pages
git add -A && git -c user.name="Mikhail Drozdov" -c user.email="mboger777@gmail.com" \
  commit -qm "Сборка сайта $(date +%F)"
git push -q --force "https://github.com/$РЕПО.git" gh-pages
cd / && rm -rf "$ВРЕМЕННО"
echo "Готово → https://s5hyhbpftv-alt.github.io/sunc-10l/"
