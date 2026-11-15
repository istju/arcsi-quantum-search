#!/usr/bin/env python3
import os
import sys
import platform
import subprocess
from pathlib import Path

def main():
    print("========================================")
    print("  ARCSI QUANTUM SEARCH - Telepítő")
    print("========================================")
    
    os_type = platform.system()
    is_termux = "com.termux" in os.environ.get("PREFIX", "")
    
    target_dir = Path(__file__).parent.parent.resolve()
    engine_dir = target_dir / "engine"
    docs_dir = target_dir / "docs"

    print(f"-> Rendszer: {'Android (Termux)' if is_termux else os_type}")
    print(f"-> Telepítési hely: {target_dir}")

    # 1. Függőségek ellenőrzése
    print("\n[1/3] Függőségek ellenőrzése...")
    try:
        subprocess.run(["python3", "-c", "import watchdog"], check=True, capture_output=True)
        print("  ✅ Python watchdog: OK")
    except subprocess.CalledProcessError:
        print("  ⚠️ Python watchdog hiányzik! Telepítsd: pip install watchdog")

    # 2. Automatikus indítás beállítása
    print("\n[2/3] Automatikus indítás beállítása...")
    if is_termux:
        boot_dir = Path.home() / ".termux" / "boot"
        boot_dir.mkdir(parents=True, exist_ok=True)
        boot_script = boot_dir / "start.sh"
        boot_content = f"""#!/data/data/com.termux/files/usr/bin/bash
sleep 60
termux-wake-lock
cd "{engine_dir}" || exit 1
nohup python3 docs_watcher.py > /dev/null 2>&1 &
"""
        boot_script.write_text(boot_content)
        os.chmod(boot_script, 0o755)
        print(f"  ✅ Termux Boot script létrehozva: {boot_script}")
    else:
        print("  ℹ️ Linux rendszer: A watcher indításához használj systemd-t vagy futtasd kézzel:")
        print(f"     cd {engine_dir} && python3 docs_watcher.py")

    # 3. Első build futtatása
    print("\n[3/3] HTML újragenerálása...")
    os.chdir(engine_dir)
    subprocess.run([sys.executable, "build_v8.py"])
    
    print("\n========================================")
    print(" ✅ TELEPÍTÉS SIKERES!")
    print("========================================")
    print("\nKövetkező lépések:")
    print(f"1. Böngészőben nyisd meg: file://{docs_dir}/index.html")
    print("2. Ha módosítasz egy .md fájlt, indítsd el a watchert:")
    print(f"   cd {engine_dir} && python3 docs_watcher.py")

if __name__ == "__main__":
    main()
