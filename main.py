PiNetwork-Monitor/
├── README.md
├── LICENSE
├── .gitignore
├── requirements.txt
├── .env.example
├── main.py                      # entrypoint: pilih mode desktop / web / cli
├── app/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── api_client.py        # ambil data Horizon
│   │   ├── monitor.py           # logika pemantauan + cache
│   │   └── notifier.py          # Telegram/Discord/console notifier
│   ├── gui/
│   │   ├── __init__.py
│   │   └── gui_desktop.py       # Tkinter desktop app + chart
│   └── web/
│       ├── __init__.py
│       ├── dashboard.py         # Flask app
│       └── templates/
│           └── index.html
└── docker/
    ├── Dockerfile
    └── docker-compose.yml



  ---

requirements.txt

Flask>=2.2.0
requests>=2.31.0
python-dotenv>=1.0.0
rich>=13.6.0
matplotlib>=3.7.0
tk>=0.1.0; platform_system != "Windows"  # tkinter built-in on many systems


---

.env.example

# API
API_URL=https://api.testnet2.minepi.com
UPDATE_INTERVAL=60

# Notifier (optional)
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=
DISCORD_WEBHOOK_URL=


---

main.py (entrypoint — pilih mode)

#!/usr/bin/env python3
import os
from dotenv import load_dotenv

load_dotenv()

def main():
    print("Pi Network Monitor Suite")
    print("1) Desktop GUI (Tkinter)")
    print("2) Web Dashboard (Flask)")
    print("3) CLI (terminal)")
    mode = input("Choose mode [1/2/3] or use args (--gui/--web/--cli): ").strip()

    import sys
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if arg in ("--gui", "gui", "desktop"): mode = "1"
        if arg in ("--web", "web", "server"): mode = "2"
        if arg in ("--cli", "cli", "terminal"): mode = "3"

    if mode == "1":
        from app.gui import gui_desktop
        gui_desktop.run_gui()
    elif mode == "2":
        from app.web import dashboard
        dashboard.run_server()
    else:
        from app.core.monitor import run_cli_loop
        run_cli_loop()

if __name__ == "__main__":
    main()


---

app/core/api_client.py

import requests
import os

API_URL = os.getenv("API_URL", "https://api.testnet2.minepi.com")
TIMEOUT = 10

def fetch_status():
    """Return JSON dict from Horizon API or raise requests exceptions."""
    resp = requests.get(API_URL, timeout=TIMEOUT)
    resp.raise_for_status()
    return resp.json()


---

app/core/monitor.py

import time
from datetime import datetime
from .api_client import fetch_status
from .notifier import Notifier
import os

INTERVAL = int(os.getenv("UPDATE_INTERVAL", "60"))
notifier = Notifier()

def parse_summary(data):
    return {
        "horizon_version": data.get("horizon_version"),
        "core_version": data.get("core_version"),
        "current_protocol": data.get("current_protocol_version"),
        "supported_protocol": data.get("supported_protocol_version"),
        "latest_ledger": data.get("core_latest_ledger") or data.get("history_latest_ledger"),
        "last_closed": data.get("history_latest_ledger_closed_at"),
        "network_passphrase": data.get("network_passphrase"),
        "fetched_at": datetime.utcnow().isoformat() + "Z"
    }

def run_cli_loop():
    print("Starting CLI monitor. Ctrl+C to exit.")
    while True:
        try:
            raw = fetch_status()
            s = parse_summary(raw)
            print("--------------------------------------------------")
            print(f"Horizon: {s['horizon_version']} | Core: {s['core_version']}")
            print(f"Protocol: {s['current_protocol']} | Supported: {s['supported_protocol']}")
            print(f"Ledger: {s['latest_ledger']} | Closed: {s['last_closed']}")
            print(f"Fetched: {s['fetched_at']}")
            notifier.check_and_notify(s)
        except Exception as e:
            print("Error fetching status:", e)
        time.sleep(INTERVAL)


---

app/core/notifier.py

import os
import logging
import requests

logger = logging.getLogger("notifier")
logger.setLevel(logging.INFO)
if not logger.handlers:
    ch = logging.StreamHandler()
    logger.addHandler(ch)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT = os.getenv("TELEGRAM_CHAT_ID")
DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK_URL")

class Notifier:
    def __init__(self):
        self.last_protocol = None

    def _send_telegram(self, text):
        if not TELEGRAM_TOKEN or not TELEGRAM_CHAT:
            return
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        try:
            requests.post(url, data={"chat_id": TELEGRAM_CHAT, "text": text}, timeout=8)
        except Exception as e:
            logger.info("Telegram send failed: %s", e)

    def _send_discord(self, text):
        if not DISCORD_WEBHOOK:
            return
        try:
            requests.post(DISCORD_WEBHOOK, json={"content": text}, timeout=8)
        except Exception as e:
            logger.info("Discord webhook failed: %s", e)

    def check_and_notify(self, summary: dict):
        try:
            proto = summary.get("current_protocol")
            if self.last_protocol is None:
                self.last_protocol = proto
                return
            if proto != self.last_protocol:
                text = f"Pi Network protocol changed: {self.last_protocol} → {proto}"
                logger.info(text)
                self._send_telegram(text)
                self._send_discord(text)
                self.last_protocol = proto
        except Exception as e:
            logger.info("Notifier error: %s", e)


---

app/gui/gui_desktop.py (Tkinter + matplotlib simple chart)

import threading
import time
import os
from tkinter import Tk, Label, Frame, BOTH
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from ..core.api_client import fetch_status
from ..core.monitor import parse_summary

INTERVAL = int(os.getenv("UPDATE_INTERVAL", "60"))

def run_gui():
    root = Tk()
    root.title("Pi Network Monitor - Desktop")

    header = Label(root, text="Pi Testnet2 Monitor", font=("Arial", 16))
    header.pack(pady=8)

    frame = Frame(root)
    frame.pack(fill=BOTH, expand=True)

    lbl_protocol = Label(frame, text="Protocol: -", font=("Arial", 12))
    lbl_protocol.pack()
    lbl_ledger = Label(frame, text="Ledger: -", font=("Arial", 12))
    lbl_ledger.pack()
    lbl_closed = Label(frame, text="Last Closed: -", font=("Arial", 12))
    lbl_closed.pack()

    # matplotlib chart
    fig = Figure(figsize=(5,2))
    ax = fig.add_subplot(111)
    ax.set_title("Ledger over time")
    ax.set_xlabel("Samples")
    ax.set_ylabel("Ledger height")
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().pack(fill=BOTH, expand=True)

    ledger_series = []

    def update_loop():
        while True:
            try:
                raw = fetch_status()
                summary = parse_summary(raw)
                proto = summary.get("current_protocol")
                ledger = summary.get("latest_ledger")
                lbl_protocol.config(text=f"Protocol: {proto}")
                lbl_ledger.config(text=f"Ledger: {ledger}")
                lbl_closed.config(text=f"Last Closed: {summary.get('last_closed')}")
                if ledger:
                    ledger_series.append(int(ledger))
                    if len(ledger_series) > 50:
                        ledger_series.pop(0)
                    ax.clear()
                    ax.plot(ledger_series)
                    ax.set_title("Ledger over time (latest samples)")
                    canvas.draw_idle()
            except Exception as e:
                print("GUI fetch error:", e)
            time.sleep(INTERVAL)

    t = threading.Thread(target=update_loop, daemon=True)
    t.start()
    root.mainloop()


---

app/web/dashboard.py (Flask mini-dashboard)

import os
from flask import Flask, jsonify, render_template
from ..core.api_client import fetch_status
from ..core.monitor import parse_summary

def create_app():
    app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), "templates"))

    @app.route("/api/status")
    def api_status():
        try:
            raw = fetch_status()
            summary = parse_summary(raw)
            return jsonify({"ok": True, "data": summary})
        except Exception as e:
            return jsonify({"ok": False, "error": str(e)}), 500

    @app.route("/")
    def index():
        # index template will fetch /api/status via JS
        return render_template("index.html")

    return app

def run_server(host="0.0.0.0", port=5000):
    app = create_app()
    app.run(host=host, port=port, debug=False)


---

app/web/templates/index.html

<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <title>Pi Network Monitor</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 20px; }
    pre { background:#f4f4f4; padding:10px; border-radius:6px; }
  </style>
</head>
<body>
  <h1>Pi Network Monitor — Dashboard</h1>
  <div id="status">Loading...</div>
  <script>
    async function refresh(){
      const res = await fetch('/api/status');
      const json = await res.json();
      const el = document.getElementById('status');
      if(json.ok){
        const d = json.data;
        el.innerHTML = `
          <pre>
Horizon: ${d.horizon_version}
Core: ${d.core_version}
Protocol: ${d.current_protocol} (supported: ${d.supported_protocol})
Ledger: ${d.latest_ledger}
Last Closed: ${d.last_closed}
Fetched: ${d.fetched_at}
          </pre>`;
      } else {
        el.textContent = 'Error: ' + (json.error || 'unknown');
      }
    }
    refresh();
    setInterval(refresh, 60000);
  </script>
</body>
</html>


---

docker/Dockerfile (optional)

FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
ENV FLASK_APP=app.web.dashboard:create_app
EXPOSE 5000
CMD ["python","main.py","--web"]


---

.gitignore (ringkas)

__pycache__/
*.pyc
.env
venv/
.DS_Store


---

🛠️ Cara jalankan (lokal)

1. Buat virtualenv & install



python -m venv venv
source venv/bin/activate    # mac/linux
venv\Scripts\activate       # windows
pip install -r requirements.txt

2. Salin .env.example jadi .env dan isi TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID / DISCORD_WEBHOOK_URL jika mau notifikasi.


3. Jalankan:



Desktop GUI:


python main.py --gui
# atau
python app/gui/gui_desktop.py

Web Dashboard:


python main.py --web
# buka http://127.0.0.1:5000

CLI:


python main.py --cli

Docker (jalankan web mode di container):

cd docker
docker build -t pinet-monitor .
docker run -p 5000:5000 --env-file ../.env pinet-monitor


---
