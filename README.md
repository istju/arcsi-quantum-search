# Arcsi Quantum Search 🚀

**A lightweight, portable, local-first Markdown knowledge base and document manager.**

Originally designed for **Android (Termux)** but now fully portable to **Linux**. 
It runs entirely on your device, requires no internet connection, and turns your Markdown files into a beautiful, searchable web interface in real-time.

![Arcsi Quantum Search Preview](docs/PICTURES/banner.png) 


## ✨ Features

- **Zero-config & Real-time**: A Python `watchdog` monitors your `.md` files and automatically rebuilds the HTML on the fly. No manual building required.
- **Local First & Private**: 100% offline. Your data never leaves your device.
- **Instant Search**: Blazing-fast client-side search with highlighted snippets.
- **Beautiful PDF Export**: Includes a dedicated print-optimized CSS (`@media print`), so you can generate professional A4 PDF presentations directly from the browser.
- **Built-in Workspace**: Edit your Markdown files directly in the browser, and save them straight back to your local file system.
- **Custom UI**: A gorgeous glassmorphism design with custom banners and backgrounds.

## 📦 Prerequisites

You will need Python 3.9+ and the `watchdog` package.

### On Android (Termux)
```bash
pkg update
pkg install python
pip install watchdog

On Linux (Arch Linux example)

sudo pacman -S python-watchdog

(On Debian/Ubuntu: sudo apt install python3-watchdog)

🚀 Installation

    Clone the repository:
    bash

    git clone https://github.com/istju/arcsi-quantum-search.git
    cd arcsi-quantum-search

    Run the installer:
    bash

    python3 engine/install.py

    (The installer automatically sets up the boot script on Android/Termux, and generates the initial HTML files).

    Start the local server & watcher:
    bash

    cd engine
    python3 docs_watcher.py

    Open your browser and navigate to:
    👉 http://localhost:8000/index.html

📂 Project Structure

    docs/ — Your Markdown documents, images (PICTURES/), saved workspace files (WORKSPACE/), and the generated HTML.

    engine/ — The Python backend (build_v8.py, docs_watcher.py, install.py).

    README.md — This file.

    LICENSE — MIT License.

🛠️ How it works

    You add or edit a .md file in the docs/ folder.

    docs_watcher.py detects the change and triggers build_v8.py.

    build_v8.py reads all Markdown files, parses them, and injects them into the template.html.

    It generates a fresh docs/index.html.

    A local Python HTTP server (running on port 8000) serves the page and handles browser-based file saving.

📄 License

This project is licensed under the MIT License — see the LICENSE file for details.

Built with ❤️ for Markdown lovers and offline-first enthusiasts.

