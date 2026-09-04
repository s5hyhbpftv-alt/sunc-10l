#!/usr/bin/env bash
# Пересобрать книги и сайт и выложить сборку на GitHub Pages.
# Ветка gh-pages содержит только dist, исходники живут в main.
# Имена переменных латиницей: bash не принимает кириллицу в идентификаторах.
set -euo pipefail
root="$(cd "$(dirname "$0")" && pwd)"
repo="s5hyhbpftv-alt/sunc-10l"

cd "$root"
python3 книга.py
python3 книга-крафт.py
python3 build_v1.py
python3 таблица.py
python3 экспорт.py

cp "out/Расписание 10-Л — СУНЦ МГУ.pdf" web/public/pdf/10L-chernila.pdf
cp "out/Расписание 10-Л — крафт.pdf"     web/public/pdf/10L-kraft.pdf
cp out/v1-raspisanie-10L-SUNC-MGU.pdf    web/public/pdf/10L-plakat-a3.pdf
cp "out/Расписание 10-Л — таблица.pdf"   web/public/pdf/10L-tablica.pdf
cp assets/kraft.jpg                      web/public/kraft.jpg

( cd web && npm run build )

tmp="$(mktemp -d)"
cp -R web/dist/. "$tmp/"
touch "$tmp/.nojekyll"
cd "$tmp"
git init -q
git checkout -qb gh-pages
git add -A
git -c user.name="Mikhail Drozdov" -c user.email="mboger777@gmail.com" \
    commit -qm "Сборка сайта $(date +%F)"
git push -q --force "https://github.com/$repo.git" gh-pages
cd /
rm -rf "$tmp"
echo "Готово → https://s5hyhbpftv-alt.github.io/sunc-10l/"
