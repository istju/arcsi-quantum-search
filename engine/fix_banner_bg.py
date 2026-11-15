#!/usr/bin/env python3
import re
from pathlib import Path

tpl_path = Path(__file__).parent / 'template.html'
if not tpl_path.exists():
    raise SystemExit("HIBA: template.html nem található!")

tpl = tpl_path.read_text(encoding='utf-8')

# Megkeressük a .banner img blokkot, és lecseréljük a .banner konténerre, 
# így a kép helyett háttérképként jelenik meg, amit könnyű pozícionálni.
pattern = r'\.banner img\s*\{[^}]*\}'
replacement = """.banner {
    height: 180px;
    background-image: url('PICTURES/banner.png');
    background-size: cover;
    background-position: center 40%; /* Itt állítjuk be, hogy a kép melyik része látszódjon */
    border-radius: 12px;
    width: 100%;
}"""

tpl = re.sub(pattern, replacement, tpl, count=1)

# A HTML-ből kivesszük a régi <img> taget, mert most már a div háttérképeként jelenik meg
tpl = tpl.replace('<div class="banner">\n<img src="PICTURES/banner.png">\n</div>', '<div class="banner"></div>')
tpl = tpl.replace('<div class="banner">\r\n<img src="PICTURES/banner.png">\r\n</div>', '<div class="banner"></div>')

tpl_path.write_text(tpl, encoding='utf-8')
print("✅ A banner most háttérképként jelenik meg, könnyen pozícionálható.")
