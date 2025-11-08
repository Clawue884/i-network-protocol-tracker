
---

# 🛰️ Pi Testnet2 Tracker

**Pi Testnet2 Tracker** adalah alat sederhana berbasis Python untuk memantau status jaringan **Pi Testnet2 (Horizon API)** secara *real-time*.  
Proyek ini membantu pengembang dan komunitas Pioneer melacak kemajuan jaringan, versi protokol, dan status upgrade menuju **Mainnet v23** dengan akurat tanpa harus bergantung pada rumor atau sumber tidak resmi.

---

## 🚀 Fitur Utama

- 🔄 Memeriksa status *Horizon API* Testnet2
- ⚙️ Menampilkan versi *core*, *horizon*, dan *protocol*
- 🧭 Memantau nomor *ledger* terbaru dan waktu pembaruannya
- 🛡️ Validasi jaringan dan *network passphrase* (Testnet/Mainnet)
- 🕒 Output status real-time langsung dari endpoint API resmi Pi

---

## 🧩 Teknologi yang Digunakan

- **Python 3.9+**
- **Requests** (untuk HTTP API)
- **JSON** (untuk parsing data)
- **Command-line interface (CLI)**

---

## 📦 Instalasi

1. **Klon repositori ini:**
   ```bash
   git clone https://github.com/<username>/pi-testnet2-tracker.git
   cd pi-testnet2-tracker

2. Buat virtual environment (opsional tapi disarankan):

python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows


3. Instal dependensi:

pip install -r requirements.txt




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
📊 Status: STABLE - Awaiting upgrade to v23


---

🧠 Tujuan Proyek

Proyek ini dibuat untuk:

Memberikan transparansi pada kemajuan teknis jaringan Pi Testnet2.

Membantu pengembang Node, App Developers, dan Pioneers memahami kapan sistem siap untuk Open Mainnet v23.

Menjadi sumber data resmi yang otomatis dan netral.



---

🗓️ Roadmap

Tahap	Deskripsi	Status

v1.0	Tracker status Testnet2	✅ Selesai
v1.1	Tambahkan notifikasi upgrade otomatis	⏳ Dalam pengembangan
v2.0	Integrasi pelacakan Mainnet langsung	🧪 Eksperimen



---

🛠️ Kontribusi

Kontribusi terbuka untuk semua Pioneers!
Jika kamu ingin menambahkan fitur baru atau memperbaiki bug:

1. Fork repositori ini


2. Buat branch baru: git checkout -b fitur-baru


3. Lakukan perubahan dan commit: git commit -m "Tambah fitur baru"


4. Kirim pull request ke branch main




---

📜 Lisensi

Proyek ini dirilis di bawah MIT License.
Silakan gunakan, ubah, dan bagikan dengan tetap mencantumkan atribusi ke pengembang asli.


---

💫 Dibangun untuk Komunitas Pi Network

> “Transparency, Technology, and Trust — one ledger at a time.”
— Clawue dapuraset (Developer & Pioneer)




---

🌍 API Resmi yang Digunakan

Pi Testnet2 Horizon API:
https://api.testnet2.minepi.com/



---

#PiNetwork #Blockchain #Testnet2 #OpenMainnet #PiDevelopers #Python #DeFi #Web3

---
