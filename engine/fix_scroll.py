#!/usr/bin/env python3
from pathlib import Path
import re

tpl_path = Path(__file__).parent / 'template.html'
if not tpl_path.exists():
    raise SystemExit("HIBA: template.html nem található!")

tpl = tpl_path.read_text(encoding='utf-8')

# 1. A .layout (a fő konténer) ne legyen a képernyőhöz szabva, engedjük nőni
tpl = tpl.replace(
    '.layout{\n    display:flex;\n    gap:12px;\n    margin-top:12px;\n    min-height: calc(100vh - 220px);\n}',
    '.layout{\n    display:flex;\n    gap:12px;\n    margin-top:12px;\n    align-items: flex-start; /* Ne nyomja össze a paneleket */\n}'
)

# 2. A panelek ne legyenek fix magasságúak, engedjük, hogy a tartalomhoz nőjenek
tpl = re.sub(r'\.panel\{[^}]*\}', '.panel{\n    background:rgba(255,255,255,0.92);\n    backdrop-filter:blur(2px);\n    padding:12px;\n    border-radius:8px;\n    box-shadow:0 2px 4px rgba(0,0,0,.15);\n    /* Kivettük a flex column-t, hogy ne erőltesse a magasságot */\n}', tpl)

# 3. A .right (jobb oldali panel) ne legyen flex, hogy ne nyomja össze a textarea-t
tpl = tpl.replace(
    '.right{\n    flex: 7;\n    min-width: 0;\n    display: flex;\n    flex-direction: column;\n}',
    '.right{\n    flex: 7;\n    min-width: 0;\n}'
)

# 4. A szerkesztők (textarea) kapjanak vissza egy fix, de tisztességes magasságot
tpl = tpl.replace(
    '#content{\n    width:100%;\n    height:auto;\n    flex: 1 1 300px;\n    min-height: 200px;',
    '#content{\n    width:100%;\n    height:350px;'
)
tpl = tpl.replace(
    '#editor{\n    width:100%;\n    height:auto;\n    flex: 1 1 200px;\n    min-height: 150px;',
    '#editor{\n    width:100%;\n    height:250px;'
)

# 5. A Workspace elrendezés ne próbáljon kitölteni mindent
tpl = tpl.replace(
    '.workspaceLayout{\n    display:flex;\n    gap:12px;\n    flex: 1 1 auto;\n}',
    '.workspaceLayout{\n    display:flex;\n    gap:12px;\n    align-items: flex-start;\n}'
)

tpl_path.write_text(tpl, encoding='utf-8')
print("✅ A görgetés és a panelek magassága visszaállítva!")
