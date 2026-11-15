#!/usr/bin/env python3
import re
from pathlib import Path

tpl_path = Path(__file__).parent / 'template.html'
if not tpl_path.exists():
    raise SystemExit("HIBA: template.html nem található!")

tpl = tpl_path.read_text(encoding='utf-8')

# Megkeressük a .banner img blokkot és beállítjuk a tökéletes eltolást
pattern = r'\.banner img\s*\{[^}]*\}'
replacement = """.banner {
    height: 180px;
    overflow: hidden;
    border-radius: 12px;
}
.banner img{
    width: 100%;
    height: auto;
    margin-top: -30px; /* A képet 30 pixellel feljebb toljuk, hogy a felirat látszódjon */
    display: block;
}"""

tpl = re.sub(pattern, replacement, tpl, count=1)

tpl_path.write_text(tpl, encoding='utf-8')
print("✅ A banner konténer rögzített magasságú, a kép pedig el van tolva.")
