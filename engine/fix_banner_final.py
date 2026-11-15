#!/usr/bin/env python3
from pathlib import Path

tpl_path = Path(__file__).parent / 'template.html'
if not tpl_path.exists():
    raise SystemExit("HIBA: template.html nem található!")

tpl = tpl_path.read_text(encoding='utf-8')

# 1. Kivesszük a korábbi margó próbálkozást a banner-ből
tpl = tpl.replace('.banner{\n    margin-top: 50px; /* Ezzel csúsztatjuk le a bannert a böngésző címsora alá */\n}\n', '')

# 2. Visszaállítjuk a body margót (hogy a háttérkép kitölthesse az egészet)
tpl = tpl.replace('margin:0;\n    padding: 0;', 'margin:0;\n    padding: 0;')

# 3. Beszúrunk egy fehér "térkitöltőt" (spacer) közvetlenül a banner elé
# Ez a legtetejére kerül, és lejjebb tolja a bannert.
tpl = tpl.replace('<div class="banner">', '<div style="height: 60px; width: 100%; background: white; /* A böngésző teteje alatti tér kitöltése */"></div>\n\n<div class="banner">')

# 4. A banner magasságát 220px-re állítjuk (elegendő ahhoz, hogy a felirat teljesen látszódjon)
tpl = tpl.replace('height:250px;', 'height:220px;')

tpl_path.write_text(tpl, encoding='utf-8')
print("✅ A banner elé bekerült egy 60px-es térkitöltő, a banner magassága pedig 220px.")
