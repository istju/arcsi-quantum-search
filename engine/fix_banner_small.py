#!/usr/bin/env python3
from pathlib import Path

tpl_path = Path(__file__).parent / 'template.html'
if not tpl_path.exists():
    raise SystemExit("HIBA: template.html nem található!")

tpl = tpl_path.read_text(encoding='utf-8')

# 1. Kivesszük a korábbi fehér térkitöltőt (spacer)
tpl = tpl.replace('<div style="height: 60px; width: 100%; background: white; /* A böngésző teteje alatti tér kitöltése */"></div>\n\n', '')

# 2. Kivesszük a korábbi margin-top-ot a banner-ből (ha benne maradt)
tpl = tpl.replace('.banner{\n    margin-top: 50px;\n}\n', '')

# 3. A banner kép beállítása: 
#    - width: 100% (hogy kitöltse a szélességet)
#    - height: auto (hogy megtartsa az eredeti arányokat)
#    - max-height: 120px (hogy biztosan beférjen és ne vágódjon le)
old_css = '.banner img{\n    width:100%;\n    height:220px;\n    object-fit:cover;'
new_css = '.banner img{\n    width:100%;\n    height:auto;\n    max-height:120px;\n    object-fit:contain;'

if old_css in tpl:
    tpl = tpl.replace(old_css, new_css)
elif '.banner img{\n    width:100%;\n    height:250px;' in tpl:
    tpl = tpl.replace('.banner img{\n    width:100%;\n    height:250px;', new_css)
else:
    # Ha valamiért nem találná a pontos szöveget, próbáljuk meg egy általánosabb cserével
    tpl = tpl.replace('height:180px;', 'height:auto; max-height:120px;')
    tpl = tpl.replace('height:250px;', 'height:auto; max-height:120px;')
    tpl = tpl.replace('height:220px;', 'height:auto; max-height:120px;')

tpl_path.write_text(tpl, encoding='utf-8')
print("✅ A banner képe most már automatikusan méreteződik, maximum 120px magas.")
