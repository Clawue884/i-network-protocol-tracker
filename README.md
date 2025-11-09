
🛰️ Pi Testnet2 Tracker  

[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Build](https://img.shields.io/badge/build-passing-brightgreen.svg)](#)
[![Status](https://img.shields.io/badge/Pi%20Protocol-v19-orange)](https://api.testnet2.minepi.com)
[![Network](https://img.shields.io/badge/Network-Pi%20Testnet2-lightblue)](https://minepi.com)

---

**Pi Testnet2 Tracker** adalah alat berbasis Python untuk memantau status jaringan **Pi Testnet2 (Horizon API)** secara *real-time*.  
Proyek ini membantu pengembang dan komunitas Pioneer melacak kemajuan jaringan, versi protokol, dan status upgrade menuju **Open Mainnet v23** dengan akurat tanpa harus bergantung pada rumor.

---

## 🚀 Fitur Utama

- 🔄 Memeriksa status *Horizon API* Testnet2  
- ⚙️ Menampilkan versi *core*, *horizon*, dan *protocol*  
- 🧭 Memantau nomor *ledger* terbaru dan waktu pembaruannya  
- 🛡️ Validasi jaringan dan *network passphrase*  
- 🕒 Pembaruan real-time setiap 1 menit  

---

## 🧩 Teknologi yang Digunakan

- **Python 3.9+**  
- **Requests** (untuk HTTP API)  
- **Colorama** (untuk tampilan warna di CLI)

---

Project structure

pi-testnet-monitor-suite/
├── README.md
├── LICENSE
├── .gitignore
├── requirements.txt
├── main.py
├── core/
│   ├── __init__.py
│   ├── api_client.py
│   ├── data_parser.py
│   └── notifier.py
├── interfaces/
│   ├── __init__.py
│   ├── cli_tracker.py
│   ├── gui_terminal.py
│   └── gui_desktop.py
└── utils/
    ├── __init__.py
    ├── config.py
    └── logger.py


---

Files

README.md

# Pi Testnet Monitor Suite

A modular monitor for Pi Network Testnet2 — CLI, terminal GUI (Rich), and optional desktop GUI.

## Quickstart

1. Clone repo
```bash
git clone https://github.com/<username>/pi-testnet-monitor-suite.git
cd pi-testnet-monitor-suite

2. Create virtualenv & install:



python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

3. Run:



python main.py

Components

core — API client, parser, notifier

interfaces — CLI, terminal GUI (Rich), desktop GUI (Tkinter)

utils — configuration & logging


License: MIT




---

LICENSE

MIT License

Copyright (c) 2025 Clawue Gabus

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


---

.gitignore

__pycache__/
*.pyc
.env
venv/
.DS_Store
.idea/
.vscode/


---

requirements.txt

requests>=2.31.0
rich>=13.6.0
pyqt6>=6.7.0; optional


---

main.py

from interfaces import cli_tracker, gui_terminal, gui_desktop
from utils.config import DEFAULTS

def main():
    print("=== Pi Testnet Monitor Suite ===")
    print("1. CLI Mode (simple)")
    print("2. GUI Terminal Mode (Rich)")
    print("3. Desktop GUI Mode (Tkinter)")
    choice = input("Pilih mode: ")

    if choice == "1":
        cli_tracker.run()
    elif choice == "2":
        gui_terminal.main()
    elif choice == "3":
        gui_desktop.run()
    else:
        print("Pilihan tidak valid.")

if __name__ == "__main__":
    main()


---

core/__init__.py

# core package


---

core/api_client.py

import requests
from utils.config import DEFAULTS

API_URL = DEFAULTS.get('API_URL')
TIMEOUT = DEFAULTS.get('TIMEOUT', 10)


def fetch_status():
    """Fetch network status from Horizon API. Returns dict or None on error."""
    try:
        r = requests.get(API_URL, timeout=TIMEOUT)
        r.raise_for_status()
        return r.json()
    except requests.RequestException:
        return None


---

core/data_parser.py

from datetime import datetime


class NetworkStatus:
    def __init__(self, raw):
        self.raw = raw or {}
        self.horizon_version = self.raw.get('horizon_version')
        self.core_version = self.raw.get('core_version')
        self.current_protocol = self.raw.get('current_protocol_version')
        self.supported_protocol = self.raw.get('supported_protocol_version')
        self.latest_ledger = self.raw.get('core_latest_ledger') or self.raw.get('history_latest_ledger')
        self.last_closed = self.raw.get('history_latest_ledger_closed_at')
        self.network_passphrase = self.raw.get('network_passphrase')

    def summary(self):
        return {
            'horizon_version': self.horizon_version,
            'core_version': self.core_version,
            'current_protocol': self.current_protocol,
            'supported_protocol': self.supported_protocol,
            'latest_ledger': self.latest_ledger,
            'last_closed': self.last_closed,
            'network_passphrase': self.network_passphrase,
            'fetched_at': datetime.utcnow().isoformat() + 'Z'
        }


---

core/notifier.py

import logging
from utils.config import DEFAULTS


class Notifier:
    def __init__(self):
        self.last_protocol = None
        self.logger = logging.getLogger('notifier')

    def check_and_notify(self, status_summary):
        """Check for protocol changes and send notification (placeholder)."""
        proto = status_summary.get('current_protocol')
        if proto is None:
            return

        if self.last_protocol is None:
            self.last_protocol = proto
            return

        if proto != self.last_protocol:
            # placeholder: extend to Telegram/Discord webhook
            self.logger.info(f'Protocol changed: {self.last_protocol} -> {proto}')
            print(f"[NOTIFY] Protocol changed: {self.last_protocol} -> {proto}")
            self.last_protocol = proto


---

interfaces/__init__.py

# interfaces package


---

interfaces/cli_tracker.py

from core.api_client import fetch_status
from core.data_parser import NetworkStatus
from core.notifier import Notifier
import time

NOTIF = Notifier()


def run(interval=60):
    print('Starting CLI tracker (press Ctrl+C to stop)')
    try:
        while True:
            raw = fetch_status()
            ns = NetworkStatus(raw)
            s = ns.summary()
            print('---')
            print(f"Horizon: {s['horizon_version']} | Core: {s['core_version']}")
            print(f"Protocol: {s['current_protocol']} | Supported: {s['supported_protocol']}")
            print(f"Ledger: {s['latest_ledger']} | Closed: {s['last_closed']}")
            NOTIF.check_and_notify(s)
            time.sleep(interval)
    except KeyboardInterrupt:
        print('\nStopped by user')


---

interfaces/gui_terminal.py

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import track
from datetime import datetime
from core.api_client import fetch_status
from core.data_parser import NetworkStatus
from core.notifier import Notifier
import time

console = Console()
NOTIF = Notifier()


def display_status(ns: NetworkStatus):
    table = Table(title="Pi Testnet2 Network Status")
    table.add_column("Parameter")
    table.add_column("Value")

    s = ns.summary()
    table.add_row("Horizon Version", str(s['horizon_version']))
    table.add_row("Core Version", str(s['core_version']))
    table.add_row("Current Protocol", str(s['current_protocol']))
    table.add_row("Supported Protocol", str(s['supported_protocol']))
    table.add_row("Latest Ledger", str(s['latest_ledger']))
    table.add_row("Last Closed", str(s['last_closed']))
    table.add_row("Network Passphrase", str(s['network_passphrase']))

    console.print(table)

    proto = s['current_protocol']
    if proto == 19:
        msg = "[yellow]Testnet masih di v19 - menunggu upgrade ke v23[/yellow]"
    elif proto >= 23:
        msg = "[green]Testnet telah diupgrade ke v23 - menuju Mainnet![/green]"
    else:
        msg = "[red]Versi tidak dikenali[/red]"

    console.print(Panel(msg, title=f"Updated: {datetime.utcnow().isoformat()}Z"))


def main(interval=60):
    last_protocol = None
    while True:
        for _ in track(range(1), description='Fetching status...'):
            raw = fetch_status()
            ns = NetworkStatus(raw)
            console.clear()
            display_status(ns)
            NOTIF.check_and_notify(ns.summary())
        time.sleep(interval)


---

interfaces/gui_desktop.py

# Minimal Tkinter desktop GUI (optional). Run only if Tkinter is available.
try:
    import tkinter as tk
    from tkinter import ttk
    from core.api_client import fetch_status
    from core.data_parser import NetworkStatus
    import threading
    import time

    def _update_label(lbl, text):
        lbl.config(text=text)

    def _fetch_loop(labels, interval):
        while True:
            raw = fetch_status()
            ns = NetworkStatus(raw)
            summary = ns.summary()
            _update_label(labels['protocol'], f"Protocol: {summary['current_protocol']}")
            _update_label(labels['ledger'], f"Ledger: {summary['latest_ledger']}")
            time.sleep(interval)

    def run(interval=60):
        root = tk.Tk()
        root.title('Pi Testnet Monitor')
        frame = ttk.Frame(root, padding=10)
        frame.pack()

        labels = {}
        labels['protocol'] = ttk.Label(frame, text='Protocol: -')
        labels['protocol'].pack()
        labels['ledger'] = ttk.Label(frame, text='Ledger: -')
        labels['ledger'].pack()

        t = threading.Thread(target=_fetch_loop, args=(labels, interval), daemon=True)
        t.start()
        root.mainloop()

except Exception as e:
    def run(*args, **kwargs):
        print('Desktop GUI not available:', e)


---

utils/__init__.py

# utils package


---

utils/config.py

DEFAULTS = {
    'API_URL': 'https://api.testnet2.minepi.com',
    'TIMEOUT': 10,
    'INTERVAL': 60
}


---

utils/logger.py

import logging

def setup_logging():
    logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s')
    return logging.getLogger()


---

Next steps

1. Copy each file into the corresponding path in your local repo.


2. git add . && git commit -m "Initial project scaffold" then push to GitHub.


3. Run python main.py and choose the interface to run.



---

⚙️ Penggunaan

Jalankan perintah berikut di terminal:

python pi_testnet_tracker.py

Contoh output:

🌐 Pi Testnet2 Network Status
---------------------------------
✅ Horizon Version: 2.23.1
✅ Core Version: stellar-core 19.6.0
✅ Current Protocol: 19
✅ Supported Protocol: 19
✅ Latest Ledger: 6157217
✅ Last Closed: 2025-11-07T00:47:04Z
🪐 Network Passphrase: Pi Testnet
---------------------------------
📊 Status: 🕓 Testnet masih di v19 - menunggu upgrade ke v23




🌍 API Resmi

Pi Testnet2 Horizon API:
https://api.testnet2.minepi.com
