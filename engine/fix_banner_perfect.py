#!/usr/bin/env python3
import re
from pathlib import Path

tpl_path = Path(__file__).parent / 'template.html'
if not tpl_path.exists():
    raise SystemExit("HIBA: template.html nem található!")

tpl = tpl_path.read_text(encoding='utf-8')

# Megkeressük a .banner img blokkot és beállítjuk a tökéletes pozíciót
pattern = r'\.banner img\s*\{[^}]*\}'
replacement = """.banner img{
    width: 100%;
    height: 180px;
    object-fit: cover;
    object-position: center 30%; /* A kép tetejétől számított 30%-nál tartja a fókuszt, így a felirat látszik */
    border-radius: 12px;
    display: block;
}"""

tpl = re.sub(pattern, replacement, tpl, count=1)

tpl_path.write_text(tpl, encoding='utf-8')
print("✅ A banner kép beállítva: a fókusz a kép felső 30%-án van.")
