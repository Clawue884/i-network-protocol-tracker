import requests
import time
from rich.console import Console
from rich.table import Table
from rich.progress import track
from rich.panel import Panel
from datetime import datetime

API_URL = "https://api.testnet2.minepi.com"
console = Console()

def fetch_status():
    """Ambil data status dari Horizon Pi Testnet2 API"""
    try:
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        console.print(f"[red]❌ Gagal menghubungi API Horizon:[/red] {e}")
        return None

def display_status(data):
    """Tampilkan status jaringan Pi Testnet2 dalam format tabel interaktif"""
    table = Table(title="🛰️ Pi Testnet2 Network Status", style="bold cyan")
    table.add_column("Parameter", justify="left", style="white", no_wrap=True)
    table.add_column("Value", justify="left", style="bold green")

    table.add_row("Horizon Version", data.get("horizon_version", "Unknown"))
    table.add_row("Core Version", data.get("core_version", "Unknown"))
    table.add_row("Current Protocol", str(data.get("current_protocol_version", "Unknown")))
    table.add_row("Supported Protocol", str(data.get("supported_protocol_version", "Unknown")))
    table.add_row("Latest Ledger", str(data.get("core_latest_ledger", "Unknown")))
    table.add_row("Last Closed", data.get("history_latest_ledger_closed_at", "Unknown"))
    table.add_row("Network Passphrase", data.get("network_passphrase", "Unknown"))

    console.print(table)

    # Status logic
    protocol = data.get("current_protocol_version", 0)
    if protocol == 19:
        message = "[yellow]🕓 Testnet masih di v19 - menunggu upgrade ke v23[/yellow]"
    elif protocol >= 23:
        message = "[green]🚀 Testnet telah diupgrade ke v23 - menuju Mainnet![/green]"
    else:
        message = "[red]⚠️ Versi tidak dikenali[/red]"

    console.print(Panel(message, expand=False, border_style="bold magenta"))

def main():
    console.clear()
    console.rule("[bold magenta]🚀 Pi Testnet2 Tracker - GUI Mode[/bold magenta]")

    last_protocol = None

    while True:
        for _ in track(range(1), description="🔄 Memeriksa status jaringan..."):
            data = fetch_status()
            if data:
                console.clear()
                console.rule(f"[bold cyan]📡 Pembaruan: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}[/bold cyan]")
                display_status(data)

                # Cek perubahan protokol
                current_protocol = data.get("current_protocol_version", 0)
                if current_protocol != last_protocol and last_protocol is not None:
                    console.print(Panel(f"[bold green]🎉 Versi protokol berubah: {last_protocol} → {current_protocol}[/bold green]", border_style="green"))
                last_protocol = current_protocol
            else:
                console.print("[red]⚠️ Tidak ada data yang dapat ditampilkan.[/red]")
        time.sleep(60)

if __name__ == "__main__":
    main()
