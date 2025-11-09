#!/usr/bin/env python3
# Pi Testnet Monitor App — All-in-One Version
# Author: Clawue Gabus (c) 2025 | License: MIT

import sys
import time
import json
import requests
from datetime import datetime

# ========== Terminal UI (Rich) ==========
try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.progress import track
    USE_RICH = True
except ImportError:
    USE_RICH = False

# ========== GUI Desktop (Tkinter) ==========
try:
    import tkinter as tk
    from tkinter import ttk
    GUI_AVAILABLE = True
except Exception:
    GUI_AVAILABLE = False


# ========== Konfigurasi ==========
API_URL = "https://api.testnet2.minepi.com"
REFRESH_INTERVAL = 60  # detik


# ========== Fungsi dasar API ==========
def fetch_status():
    """Ambil status jaringan dari Horizon Pi Testnet2."""
    try:
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"error": str(e)}


def parse_status(data):
    """Ambil informasi utama dari JSON API."""
    return {
        "horizon_version": data.get("horizon_version"),
        "core_version": data.get("core_version"),
        "current_protocol": data.get("current_protocol_version"),
        "supported_protocol": data.get("supported_protocol_version"),
        "latest_ledger": data.get("core_latest_ledger") or data.get("history_latest_ledger"),
        "last_closed": data.get("history_latest_ledger_closed_at"),
        "network_passphrase": data.get("network_passphrase"),
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


# ========== CLI sederhana ==========
def run_cli():
    print("=== Pi Testnet2 Monitor (CLI Mode) ===")
    while True:
        data = fetch_status()
        if "error" in data:
            print(f"[ERROR] {data['error']}")
        else:
            s = parse_status(data)
            print("----------------------------------------")
            print(f"Horizon: {s['horizon_version']} | Core: {s['core_version']}")
            print(f"Protocol: {s['current_protocol']} (Supported: {s['supported_protocol']})")
            print(f"Ledger: {s['latest_ledger']} | Closed: {s['last_closed']}")
            print(f"Passphrase: {s['network_passphrase']}")
            print(f"Updated: {s['timestamp']}")
            print("----------------------------------------")
        time.sleep(REFRESH_INTERVAL)


# ========== Terminal interaktif (Rich) ==========
def run_rich():
    console = Console()
    console.print("[bold magenta]🚀 Pi Testnet2 Monitor (Rich Mode)[/bold magenta]\n")

    while True:
        for _ in track(range(1), description="Fetching status..."):
            data = fetch_status()
            if "error" in data:
                console.print(f"[red]Error:[/red] {data['error']}")
                time.sleep(REFRESH_INTERVAL)
                continue

            s = parse_status(data)
            console.clear()
            table = Table(title="Pi Testnet2 Network Status")
            table.add_column("Parameter")
            table.add_column("Value")

            table.add_row("Horizon Version", str(s["horizon_version"]))
            table.add_row("Core Version", str(s["core_version"]))
            table.add_row("Current Protocol", str(s["current_protocol"]))
            table.add_row("Supported Protocol", str(s["supported_protocol"]))
            table.add_row("Latest Ledger", str(s["latest_ledger"]))
            table.add_row("Last Closed", str(s["last_closed"]))
            table.add_row("Network Passphrase", str(s["network_passphrase"]))
            console.print(table)

            proto = s["current_protocol"]
            if proto == 19:
                msg = "[yellow]🕓 Testnet masih di v19 - menunggu upgrade ke v23[/yellow]"
            elif proto and proto >= 23:
                msg = "[green]🚀 Testnet telah diupgrade ke v23 - menuju Mainnet![/green]"
            else:
                msg = "[red]⚠️ Versi tidak dikenali[/red]"

            console.print(Panel(msg, title=f"Last Update: {s['timestamp']}"))
            time.sleep(REFRESH_INTERVAL)


# ========== GUI Desktop (Tkinter) ==========
def run_gui():
    root = tk.Tk()
    root.title("Pi Testnet2 Monitor")
    frame = ttk.Frame(root, padding=20)
    frame.pack(fill="both", expand=True)

    title = ttk.Label(frame, text="🚀 Pi Testnet2 Network Monitor", font=("Arial", 14, "bold"))
    title.pack(pady=5)

    labels = {}
    for key in ["Protocol", "Ledger", "Last Closed", "Status"]:
        labels[key] = ttk.Label(frame, text=f"{key}: -", font=("Arial", 11))
        labels[key].pack(pady=2)

    def update_loop():
        while True:
            data = fetch_status()
            if "error" not in data:
                s = parse_status(data)
                labels["Protocol"].config(text=f"Protocol: {s['current_protocol']}")
                labels["Ledger"].config(text=f"Ledger: {s['latest_ledger']}")
                labels["Last Closed"].config(text=f"Closed: {s['last_closed']}")
                if s["current_protocol"] == 19:
                    labels["Status"].config(text="🕓 Testnet masih di v19 - menunggu upgrade ke v23")
                elif s["current_protocol"] and s["current_protocol"] >= 23:
                    labels["Status"].config(text="🚀 Sudah di v23 - menuju Mainnet!")
                else:
                    labels["Status"].config(text="⚠️ Versi tidak dikenali")
            time.sleep(REFRESH_INTERVAL)

    import threading
    threading.Thread(target=update_loop, daemon=True).start()
    root.mainloop()


# ========== Entry Point ==========
def main():
    print("=== Pi Testnet2 Monitor ===")
    print("1. CLI Mode")
    print("2. Rich Terminal Mode")
    print("3. GUI Desktop Mode\n")

    # Pilih otomatis jika ada argumen
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
    else:
        mode = input("Pilih mode [1/2/3]: ").strip()

    if mode in ["1", "cli", "--cli"]:
        run_cli()
    elif mode in ["2", "rich", "--rich"]:
        if USE_RICH:
            run_rich()
        else:
            print("Rich tidak terpasang. Jalankan: pip install rich")
            run_cli()
    elif mode in ["3", "gui", "--gui"]:
        if GUI_AVAILABLE:
            run_gui()
        else:
            print("Tkinter tidak tersedia di lingkungan ini.")
            run_cli()
    else:
        print("Pilihan tidak dikenali.")
        run_cli()


if __name__ == "__main__":
    main()
