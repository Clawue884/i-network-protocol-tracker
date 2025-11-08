
# 🛰️ Pi Network Protocol Tracker

**Pi Network Protocol Tracker** adalah alat open-source berbasis Python yang memantau status *real-time* dari jaringan **Pi Testnet2** dan **Mainnet** melalui **Horizon API resmi**.  
Proyek ini memungkinkan pengembang dan komunitas Pi untuk melacak:
- Versi protokol (`v19`, `v23`, dst)
- Versi Stellar-Core dan Horizon
- Aktivitas ledger terbaru
- Sinkronisasi node secara langsung
- Visualisasi data jaringan (grafik waktu nyata)

---

## 🚀 Fitur Utama

✅ **Pemantauan langsung** versi protokol dari jaringan Pi Network  
📡 **Koneksi langsung** ke endpoint Horizon API resmi (`https://api.testnet2.minepi.com/`)  
📈 **Grafik interaktif** ledger & perubahan versi (menggunakan Matplotlib)  
⚙️ **Dapat dikonfigurasi** untuk Testnet atau Mainnet  
🧠 **Mudah diperluas** — bisa diintegrasikan dengan dashboard web, Telegram bot, atau sistem notifikasi

---

## 🧩 Arsitektur Sederhana

┌────────────────────────────────┐ │ Horizon API (Pi Testnet/Mainnet)│ └──────────────┬─────────────────┘ │ JSON Data ▼ [ pi_network_tracker.py ] │ ▼ Ledger Graph  ←→  Protocol Graph

---

## 🧠 Prasyarat

Pastikan Python 3.8+ sudah terinstal di sistem kamu.

### Instalasi Dependensi
```bash
pip install requests matplotlib


---

⚙️ Cara Menjalankan

1. Clone repositori ini

git clone https://github.com/<username>/pi-network-protocol-tracker.git
cd pi-network-protocol-tracker


2. Jalankan script utama

python pi_network_tracker.py


3. Lihat hasilnya

Data status jaringan akan muncul di terminal (CLI)

Dua grafik akan terbuka otomatis:

📈 Ledger Height (aktivitas jaringan)

🔸 Protocol Version (perubahan versi)






---

🧭 Contoh Output

Terminal

🔗 Jaringan: Pi Testnet
🌍 URL: https://api.testnet2.minepi.com
-----------------------------------------------
📘 Horizon Version: 2.23.1
⚙️ Core Version: stellar-core 19.6.0
📡 Current Protocol Version: 19
🕓 Latest Ledger: 6157217
📅 Closed At: 2025-11-07T00:47:04Z
✅ Node Sinkron & Aktif

Grafik

Grafik 1: Ledger Height (menunjukkan aktivitas blockchain)

Grafik 2: Protocol Version (akan berubah saat upgrade ke v23)



---

🔄 Konfigurasi Jaringan

Ubah jaringan dari Testnet ke Mainnet di dalam kode:

NETWORK = "mainnet"  # default: testnet2


---

💡 Rencana Pengembangan

[ ] Notifikasi otomatis saat protokol berubah (email / Telegram)

[ ] Penyimpanan data historis (SQLite / CSV)

[ ] Dashboard web interaktif (Flask / React)

[ ] Integrasi AI untuk deteksi anomali jaringan



---

🧑‍💻 Kontribusi

Kontribusi sangat diterima!
Silakan fork repositori ini dan buat pull request untuk fitur tambahan atau perbaikan bug.

Langkah umum:

git checkout -b fitur-baru
git commit -m "Menambahkan fitur notifikasi"
git push origin fitur-baru


---

🛡️ Lisensi

Proyek ini dirilis di bawah lisensi MIT License — bebas digunakan, dimodifikasi, dan dikembangkan dengan menyertakan atribusi ke pembuat asli.


---

🌐 Kredit & Referensi

Pi Network Official Site

Horizon API Documentation

Stellar Core Protocol

Matplotlib



---

> 🪐 Developed with ❤️ for the global Pi Network community.
Stay patient, stay building — the Open Mainnet will come when the ecosystem is ready. 🚀



---

Apakah kamu mau saya bantu sekalian buatkan **struktur folder GitHub lengkap (kode + readme + license + .gitignore)** supaya kamu tinggal `git push` saja ke repositori barumu `pi-network-protocol-tracker`?
