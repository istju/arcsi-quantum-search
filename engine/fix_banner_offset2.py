#!/usr/bin/env python3
import re
from pathlib import Path

tpl_path = Path(__file__).parent / 'template.html'
if not tpl_path.exists():
    raise SystemExit("HIBA: template.html nem található!")

tpl = tpl_path.read_text(encoding='utf-8')

# Megkeressük a .banner img blokkot és feljebb toljuk a képet
pattern = r'\.banner img\s*\{[^}]*\}'
replacement = """.banner {
    height: 180px;
    overflow: hidden;
    border-radius: 12px;
    display: flex;
    align-items: flex-start;
}
.banner img{
    width: 100%;
    height: auto;
    margin-top: -80px; /* A képet 80 pixellel toljuk feljebb */
    display: block;
}"""

tpl = re.sub(pattern, replacement, tpl, count=1)

tpl_path.write_text(tpl, encoding='utf-8')
print("✅ A banner kép -80px eltolással.")
