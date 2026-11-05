# GAMEVERSE – Steam Gaming Analytics Dashboard

Dashboard interaktif untuk eksplorasi katalog game Steam. Proyek ini dibuat untuk memenuhi komponen UTS Visualisasi Data: KPI, variasi grafik, filter interaktif, desain visual, dan storytelling/insight.

## Dataset
- Sumber: [Steam Store Games – Kaggle](https://www.kaggle.com/datasets/nikdavis/steam-store-games)
- File utama yang diberikan: `steam.csv`
- Jumlah data awal: **27.075 baris dan 18 kolom**
- File tambahan dalam ZIP asli (deskripsi, media, requirements, support, tag) tidak diperlukan untuk dashboard dasar ini.
- Dataset merupakan snapshot historis, bukan data real-time.

## Fitur dashboard
- 4 KPI: total game, rata-rata harga, rata-rata rating positif, total ulasan.
- 5 visualisasi: bar chart genre, line chart tren rilis, donut chart free vs paid, scatter harga vs rating, histogram waktu bermain.
- Filter interaktif: rentang tahun, genre, jenis harga, dan platform.
- Insight otomatis yang berubah mengikuti filter.
- Tabel 10 game dengan jumlah ulasan terbanyak.

## Struktur folder
```text
GAMEVERSE_UTS/
├── app.py
├── requirements.txt
├── README.md
└── dataset/
    ├── steam_raw.csv
    └── steam_clean.csv
```

## Menjalankan di komputer lokal
Disarankan menggunakan Python 3.10 atau lebih baru.

1. Ekstrak ZIP proyek.
2. Buka terminal/PowerShell pada folder `GAMEVERSE_UTS`.
3. Buat virtual environment (opsional tetapi disarankan):
   ```bash
   python -m venv .venv
   ```
4. Aktifkan environment:
   - Windows PowerShell: `.venv\Scripts\Activate.ps1`
   - Windows CMD: `.venv\Scripts\activate.bat`
5. Instal library:
   ```bash
   pip install -r requirements.txt
   ```
6. Jalankan dashboard:
   ```bash
   streamlit run app.py
   ```
7. Browser akan membuka alamat lokal Streamlit (biasanya `http://localhost:8501`).

## Deploy ke Streamlit Community Cloud
1. Buat repository GitHub baru dan set **Public**.
2. Upload `app.py`, `requirements.txt`, `README.md`, dan folder `dataset/`.
3. Buka https://share.streamlit.io/ dan hubungkan GitHub.
4. Pilih repository, branch, dan file utama `app.py`.
5. Deploy. Setelah selesai, salin URL dashboard ke README.

## Catatan interpretasi
- `positive_rate` adalah persentase ulasan positif dari total ulasan, bukan skor resmi Steam.
- `owners` pada dataset berupa rentang estimasi. Kolom `owners_estimated` hanya titik tengah rentang dan tidak dipakai sebagai angka pengguna pasti.
- Nilai `average_playtime` pada sumber dalam menit; dashboard mengubahnya menjadi jam.
- Tahun rilis yang tidak terbaca diberi nilai 0 pada file hasil cleaning dan dikecualikan dari grafik tren.
- Angka harga menggunakan mata uang sebagaimana tercatat dalam dataset (umumnya USD pada sumber).

## Identitas mahasiswa
Lengkapi nama, NPM, kelas, dan dosen pada bagian ini sebelum pengumpulan.
