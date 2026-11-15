#!/usr/bin/env python3
import re
from pathlib import Path

tpl_path = Path(__file__).parent / 'template.html'
if not tpl_path.exists():
    raise SystemExit("HIBA: template.html nem található!")

tpl = tpl_path.read_text(encoding='utf-8')

# 1. A .layout blokkból kivesszük a min-height / height beállításokat
# Megkeressük a .layout { ... } blokkot és kicseréljük egy egyszerűbbre
tpl = re.sub(r'\.layout\s*\{[^}]*\}', 
             '.layout {\n    display: flex;\n    gap: 12px;\n    margin-top: 12px;\n    align-items: flex-start;\n}', 
             tpl)

# 2. A .right blokkból kivesszük a flex column-t (ha még benne van)
tpl = re.sub(r'\.right\s*\{[^}]*\}', 
             '.right {\n    flex: 7;\n    min-width: 0;\n}', 
             tpl)

# 3. A .panel blokkból kivesszük a flex column-t
tpl = re.sub(r'\.panel\s*\{[^}]*\}', 
             '.panel {\n    background: rgba(255,255,255,0.92);\n    backdrop-filter: blur(2px);\n    padding: 12px;\n    border-radius: 8px;\n    box-shadow: 0 2px 4px rgba(0,0,0,.15);\n}', 
             tpl)

# 4. A textarea-knak fix magasságot adunk, hogy ne próbáljanak rugalmasan viselkedni
tpl = re.sub(r'#content\s*\{[^}]*\}', 
             '#content {\n    width: 100%;\n    height: 350px;\n    resize: vertical;\n    box-sizing: border-box;\n}', 
             tpl)

tpl = re.sub(r'#editor\s*\{[^}]*\}', 
             '#editor {\n    width: 100%;\n    height: 250px;\n    resize: vertical;\n    box-sizing: border-box;\n}', 
             tpl)

# 5. A Workspace layout is legyen flex-start
tpl = re.sub(r'\.workspaceLayout\s*\{[^}]*\}', 
             '.workspaceLayout {\n    display: flex;\n    gap: 12px;\n    align-items: flex-start;\n}', 
             tpl)

tpl_path.write_text(tpl, encoding='utf-8')
print("✅ Minden fix magasság és flex kényszer eltávolítva, a görgetés visszaállítva.")
