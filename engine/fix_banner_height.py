#!/usr/bin/env python3
from pathlib import Path

tpl_path = Path(__file__).parent / 'template.html'
if not tpl_path.exists():
    raise SystemExit("HIBA: template.html nem található!")

tpl = tpl_path.read_text(encoding='utf-8')

# 1. A banner magasságának növelése (180px -> 250px), hogy a kép ne vágódjon le
tpl = tpl.replace(
    '.banner img{\n    width:100%;\n    height:180px;',
    '.banner img{\n    width:100%;\n    height:250px;'
)

# 2. A korábbi 50px-es margó megtartása (hogy a böngésző címsora ne takarja)
# (Ez már benne van a fájlban, nem kell hozzányúlni)

tpl_path.write_text(tpl, encoding='utf-8')
print("✅ A banner magassága 250px-re növelve, hogy a felirat ne vágódjon le.")
