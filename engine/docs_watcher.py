#!/usr/bin/env python3
import http.server
import json
import os
import socketserver
import subprocess
import sys
import threading
import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

DEBOUNCE = 1.0
RELEVANT = ('.md', '.txt', '.log')
PORT = 8000  # A böngésző ezen a porton éri el

# A projekt gyökere és a docs mappa
BASE_DIR = Path(__file__).parent.parent.resolve()
DOCS_DIR = BASE_DIR / "docs"
WATCHER_SCRIPT = Path(__file__).resolve()

# --- WATCHER OSZTÁLY ---
class Handler(FileSystemEventHandler):
    def __init__(self):
        self._timer = None
        self._lock = threading.Lock()

    def _schedule(self):
        with self._lock:
            if self._timer:
                self._timer.cancel()
            self._timer = threading.Timer(DEBOUNCE, self._rebuild)
            self._timer.daemon = True
            self._timer.start()

    def _rebuild(self):
        try:
            print("[watcher] Változás észlelve, újragenerálás...")
            subprocess.run([sys.executable, str(BASE_DIR / "engine" / "build_v8.py")], check=True)
        except Exception as e:
            print(f"[watcher] hiba: {e}")

    def _ok(self, p):
        return Path(p).suffix.lower() in RELEVANT

    def on_created(self, e):
        if not e.is_directory and self._ok(e.src_path): self._schedule()
    def on_modified(self, e):
        if not e.is_directory and self._ok(e.src_path): self._schedule()
    def on_moved(self, e):
        if not e.is_directory and self._ok(e.dest_path): self._schedule()
    def on_deleted(self, e):
        if not e.is_directory and self._ok(e.src_path): self._schedule()

# --- HTTP SZERVER OSZTÁLY ---
class DocsRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DOCS_DIR), **kwargs)

    def do_POST(self):
        if self.path == '/save':
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))
                
                filename = data.get('filename')
                content = data.get('content')
                is_workspace = data.get('isWorkspace', False)

                if not filename or content is None:
                    self.send_error(400, "Missing filename or content")
                    return

                # Biztonsági ellenőrzés
                if '..' in filename or filename.startswith('/'):
                    self.send_error(400, "Invalid filename")
                    return

                target_dir = DOCS_DIR / "WORKSPACE" if is_workspace else DOCS_DIR
                target_file = target_dir / filename

                target_file.write_text(content, encoding='utf-8')

                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"success": True}).encode('utf-8'))
                print(f"[http] Mentve: {target_file.name}")
            except Exception as e:
                self.send_error(500, f"Server error: {e}")
        else:
            self.send_error(404, "Not Found")

def run_http_server():
    with socketserver.TCPServer(("", PORT), DocsRequestHandler) as httpd:
        print(f"[http] Szerver fut: http://localhost:{PORT}/index.html")
        httpd.serve_forever()

# --- MAIN ---
if __name__ == "__main__":
    print("[watcher] Kezdeti build...")
    subprocess.run([sys.executable, str(BASE_DIR / "engine" / "build_v8.py")], check=False)

    # HTTP szerver indítása külön szálon
    threading.Thread(target=run_http_server, daemon=True).start()

    # Watcher indítása
    event_handler = Handler()
    observer = Observer()
    observer.schedule(event_handler, str(DOCS_DIR), recursive=True)
    observer.start()
    print(f"[watcher] Figyelem: {DOCS_DIR}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
