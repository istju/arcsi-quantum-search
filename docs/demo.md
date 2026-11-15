# Arcsi Quantum Search

**A local-first, portable Markdown knowledge base and document manager.**

## ✨ Core Features

- **Real-time Watcher**: Python `watchdog` detects file changes and instantly rebuilds the HTML.
- **Local HTTP Server**: Built-in Python server handles saving files directly from the browser.
- **Instant Search**: Blazing-fast client-side search with highlighted snippets.
- **PDF Export**: Dedicated `@media print` CSS generates perfect A4 PDF presentations.
- **Custom UI**: Beautiful glassmorphism interface with custom banner and background.

> **Privacy First:** 100% offline. Your data never leaves your device.

## 🛠️ Technology Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Frontend** | HTML5, CSS3, Vanilla JS | Glassmorphism UI, instant search |
| **Backend** | Python 3, `watchdog` | File monitoring, local HTTP server |
| **Markdown** | `marked.js` | Fast client-side rendering |
| **Output** | CSS `@media print` | Professional A4 PDF generation |

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/istju/arcsi-quantum-search.git
cd arcsi-quantum-search

# Run the installer
python3 engine/install.py

# Start the local server and watcher
cd engine
python3 docs_watcher.py