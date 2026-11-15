#!/usr/bin/env python3
from pathlib import Path

tpl_path = Path(__file__).parent / 'template.html'
if not tpl_path.exists():
    raise SystemExit("HIBA: template.html nem található!")

tpl = tpl_path.read_text(encoding='utf-8')

# 1. Visszaállítjuk a body margót az eredetire (hogy ne legyen felesleges hézag)
tpl = tpl.replace('margin:0;\n    padding: 0;', 'margin:0;')

# 2. Kivesszük a korábbi main-wrapper-t, ha benne maradt
tpl = tpl.replace('<div class="main-wrapper">\n', '')
tpl = tpl.replace('</div>\n</div>\n\n<script>', '</div>\n\n<script>')

# 3. A .banner osztályhoz hozzáadunk egy felső margót
old_banner_css = '.banner img{\n    width:100%;'
new_banner_css = '.banner{\n    margin-top: 50px; /* Ezzel csúsztatjuk le a bannert a böngésző címsora alá */\n}\n.banner img{\n    width:100%;'

if old_banner_css in tpl:
    tpl = tpl.replace(old_banner_css, new_banner_css)
else:
    print("⚠️ Figyelmeztetés: Nem találtam a .banner img CSS-t, lehet hogy kézzel módosítva lett.")

# 4. Kivesszük a korábbi main-wrapper CSS-t, ha benne maradt
tpl = tpl.replace("""
.main-wrapper {
    padding: 40px 10px 10px 10px; /* 40px felső margó, hogy a banner ne lógjon a böngésző teteje alá */
    box-sizing: border-box;
}
""", "")

tpl_path.write_text(tpl, encoding='utf-8')
print("✅ A banner felső margója beállítva (50px), a felesleges wrapper eltávolítva.")
