#!/usr/bin/env python3
import re
from pathlib import Path

tpl_path = Path(__file__).parent / 'template.html'
if not tpl_path.exists():
    raise SystemExit("HIBA: template.html nem található!")

tpl = tpl_path.read_text(encoding='utf-8')

# Megkeressük a .banner img blokkot és feljebb toljuk a fókuszt
pattern = r'\.banner img\s*\{[^}]*\}'
replacement = """.banner img{
    width: 100%;
    height: 180px;
    object-fit: cover;
    object-position: center 10%; /* A fókusz feljebb, hogy az "ARCSI" felirat látszódjon */
    border-radius: 12px;
    display: block;
}"""

tpl = re.sub(pattern, replacement, tpl, count=1)

tpl_path.write_text(tpl, encoding='utf-8')
print("✅ A banner kép fókusza feljebb tolva (center 10%).")
