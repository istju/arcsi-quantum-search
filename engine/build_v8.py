#!/usr/bin/env python3
"""Beolvassa a DOCS mappát, és legenerálja a DOCS/index.html-t."""
import json
import sys
from pathlib import Path

# HTML entitások tisztítása (a PS1-ből)
ENTITY_FIXES = [
    ("&#x20;", " "), ("&lt;", "<"), ("&gt;", ">"), ("&amp;", "&"),
    ("\\u0026#x20;", " "), ("&amp;#x20;", " "),
    ("&amp;amp;#x20;", " "), ("&amp;amp;amp;#x20;", " "),
]

def clean(content: str) -> str:
    for old, new in ENTITY_FIXES:
        content = content.replace(old, new)
    return content

def build():
    here        = Path(__file__).parent.resolve()
    docs_folder = here.parent / 'docs'
    template    = here / 'template.html'
    output      = docs_folder / 'index.html'

    if not template.exists():
        print(f"HIBA: Nincs template.html! Futtasd előbb az extract_template.py-t!")
        return

    # 1) Fő dokumentumok (csak a DOCS gyökérben, nem rekurzívan)
    docs = []
    for f in sorted(docs_folder.iterdir()):
        if not f.is_file():
            continue
        if f.suffix.lower() not in ('.md', '.txt', '.log'):
            continue
        try:
            content = f.read_text(encoding='utf-8')
            docs.append({
                "name": f.name,
                "content": clean(content or "")
            })
        except Exception as e:
            print(f"HIBA: {f.name}: {e}")

    # 2) WORKSPACE mappa (.md fájlok, legfrissebb elöl)
    workspace = []
    ws = docs_folder / "WORKSPACE"
    if ws.is_dir():
        ws_files = sorted(
            [f for f in ws.iterdir() if f.is_file() and f.suffix.lower() == '.md'],
            key=lambda f: f.stat().st_mtime,
            reverse=True,
        )
        for f in ws_files:
            try:
                workspace.append({
                    "name": f.name,
                    "content": f.read_text(encoding='utf-8')
                })
            except Exception as e:
                print(f"HIBA (workspace): {f.name}: {e}")

    # 3) JSON generálás (mindig tömb, még 0 vagy 1 elem esetén is)
    docs_json = json.dumps(docs,      ensure_ascii=False, separators=(',', ':'))
    ws_json   = json.dumps(workspace, ensure_ascii=False, separators=(',', ':'))

    # 4) HTML összeállítása
    html = template.read_text(encoding='utf-8')
    html = html.replace('__DOCS_JSON__',      docs_json)
    html = html.replace('__WORKSPACE_JSON__', ws_json)

    # 5) Atomikus írás (temp + move), hogy a böngésző ne félkész fájlt kapjon
    tmp = output.with_suffix('.html.tmp')
    tmp.write_text(html, encoding='utf-8')
    tmp.replace(output)

    print(f"✅ index.html frissítve: {len(docs)} dok, {len(workspace)} workspace")

if __name__ == '__main__':
    build()
