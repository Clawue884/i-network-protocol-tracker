import requests
import json
import time
from colorama import Fore, Style

API_URL = "https://api.testnet2.minepi.com"

def fetch_status():
    """Ambil data status dari Horizon Pi Testnet2 API"""
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"❌ Gagal menghubungi API Horizon: {e}" + Style.RESET_ALL)
        return None

def display_status(data):
    """Tampilkan status jaringan Pi Testnet2"""
    print(Fore.CYAN + "\n🌐 Pi Testnet2 Network Status")
    print("---------------------------------" + Style.RESET_ALL)
    print(Fore.GREEN + f"✅ Horizon Version: {data.get('horizon_version', 'Unknown')}")
    print(f"✅ Core Version: {data.get('core_version', 'Unknown')}")
    print(f"✅ Current Protocol: {data.get('current_protocol_version', 'Unknown')}")
    print(f"✅ Supported Protocol: {data.get('supported_protocol_version', 'Unknown')}")
    print(f"✅ Latest Ledger: {data.get('core_latest_ledger', 'Unknown')}")
    print(f"✅ Last Closed: {data.get('history_latest_ledger_closed_at', 'Unknown')}")
    print(f"🪐 Network Passphrase: {data.get('network_passphrase', 'Unknown')}")
    print("---------------------------------" + Style.RESET_ALL)

    protocol = data.get("current_protocol_version", 0)
    if protocol == 19:
        status = "🕓 Testnet masih di v19 - menunggu upgrade ke v23"
        color = Fore.YELLOW
    elif protocol >= 23:
        status = "🚀 Testnet telah diupgrade ke v23 - menuju Mainnet!"
        color = Fore.GREEN
    else:
        status = "⚠️ Versi tidak dikenali"
        color = Fore.RED

    print(color + f"📊 Status: {status}" + Style.RESET_ALL)
    print("")

def main():
    print(Fore.MAGENTA + "🚀 Memulai Pi Testnet2 Tracker...\n" + Style.RESET_ALL)
    while True:
        data = fetch_status()
        if data:
            display_status(data)
        else:
            print(Fore.RED + "Tidak ada data yang dapat ditampilkan.\n" + Style.RESET_ALL)
        time.sleep(60)  # perbarui setiap 1 menit

if __name__ == "__main__":
    main()
