#!/usr/bin/env python3
from pathlib import Path

tpl_path = Path(__file__).parent / 'template.html'
if not tpl_path.exists():
    raise SystemExit("HIBA: template.html nem található!")

tpl = tpl_path.read_text(encoding='utf-8')

# 1. A body margójának visszaállítása (hogy a háttérkép kitölthesse az egészet)
old_css = """margin:0;
    padding: 20px 10px 10px 10px; /* Fent 20px, oldalt és lent 10px */"""
new_css = """margin:0;
    padding: 0;"""
tpl = tpl.replace(old_css, new_css)

# 2. Egy új konténer hozzáadása a banner és a layout köré
# Megkeressük a <body> elemet, és egy div-et teszünk közvetlenül utána
tpl = tpl.replace('<body>\n\n<div class="banner">', '<body>\n\n<div class="main-wrapper">\n<div class="banner">')

# 3. A legutolsó </div> (a layout lezárása) elé beszúrjuk a wrapper lezárását
# Mivel a fájl végén van a script, a layout lezárása után, de a script előtt kell lezárni.
# A layout a legkülső elem a body-ban, így a </body> elé tesszük a </div>-et
tpl = tpl.replace('</div>\n\n<script>', '</div>\n</div>\n\n<script>')

# 4. CSS hozzáadása a main-wrapper-hez
css_to_add = """
.main-wrapper {
    padding: 40px 10px 10px 10px; /* 40px felső margó, hogy a banner ne lógjon a böngésző teteje alá */
    box-sizing: border-box;
}
"""
tpl = tpl.replace('</style>', css_to_add + '</style>')

tpl_path.write_text(tpl, encoding='utf-8')
print("✅ A banner és a tartalom egy wrapper-be került, így lejjebb csúszik.")
