#!/usr/bin/env python3
from pathlib import Path

tpl_path = Path(__file__).parent / 'template.html'
if not tpl_path.exists():
    raise SystemExit("HIBA: template.html nem található!")

tpl = tpl_path.read_text(encoding='utf-8')

# A body margójának kinullázása és a banner felső margójának beállítása
old_css = """body{
    font-family:Segoe UI,Arial;
    background-image:url("PICTURES/3d-rendering-broken-glass-texture.jpg");
    background-size:cover;
    background-position:center;
    background-attachment:fixed;

    margin:10px;"""
    
new_css = """body{
    font-family:Segoe UI,Arial;
    background-image:url("PICTURES/3d-rendering-broken-glass-texture.jpg");
    background-size:cover;
    background-position:center;
    background-attachment:fixed;

    margin:0;
    padding: 20px 10px 10px 10px; /* Fent 20px, oldalt és lent 10px */
    box-sizing: border-box;"""

if old_css in tpl:
    tpl = tpl.replace(old_css, new_css)
    
    # A banner konténerének igazítása, hogy ne lógjon ki
    tpl = tpl.replace('.banner img{\n    width:100%;', '.banner img{\n    width:100%;\n    display:block;')
    
    tpl_path.write_text(tpl, encoding='utf-8')
    print("✅ A banner felső margója és a body paddingja javítva!")
else:
    print("⚠️ Nem találtam a body CSS blokkot. Lehet, hogy már módosítva lett.")
