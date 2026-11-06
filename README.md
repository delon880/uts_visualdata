# 🎮 GAMEVERSE: Steam Gaming Analytics Dashboard

**Nama:** [Dionisius Dave Abuthan]
**NIM:** [241051023]
**Mata Kuliah:** [Nama Mata Kuliah / Tugas]

---

## 🔗 Tautan Penting
- **Live Dashboard Streamlit:** (https://utsvisualdata-ajqzqwtfmxise8lstbnlvf.streamlit.app/)]
- **Dataset Kaggle:** [https://www.kaggle.com/datasets/nikdavis/steam-store-games](https://www.kaggle.com/datasets/nikdavis/steam-store-games)

---

## 📖 Latar Belakang & Key Insights
**Latar Belakang:**
Industri game di platform Steam terus berkembang pesat setiap tahunnya. Dashboard **GAMEVERSE** ini dibuat untuk membantu para developer, publisher, maupun gamer dalam memahami tren pasar. Analisis difokuskan pada eksplorasi genre, perbandingan harga (gratis vs berbayar), tren rilis dari tahun ke tahun, serta hubungan antara harga game dengan respon positif dari pemain.

**Key Insights (Wawasan Utama):**
Berdasarkan hasil visualisasi data pada dashboard, didapatkan beberapa temuan utama:
1. **Dominasi Genre:** Genre dengan jumlah judul terbanyak pada dataset adalah **Action**, menunjukkan minat pasar yang sangat tinggi terhadap game-game berskala kecil maupun aksi.
2. **Tren Rilis:** Jumlah rilis game di Steam mengalami lonjakan yang sangat masif (eksponensial) mulai dari tahun **2015** hingga tahun-tahun terakhir.
3. **Gratis vs Berbayar:** Meskipun game berbayar (Paid) jumlahnya lebih banyak, game gratis (*Free-to-Play*) cenderung memiliki jumlah ulasan (engagement) yang jauh lebih tinggi karena mudah diakses oleh semua orang.
4. **Harga vs Rating:** Harga sebuah game tidak menjamin rating yang tinggi. Banyak game dengan harga murah (di bawah $10) yang berhasil mendapatkan persentase rating positif (di atas 80%) dari para pemain.
5. **Waktu Bermain:** Mayoritas pemain menghabiskan waktu kurang dari 50 jam untuk memainkan satu game, menunjukkan bahwa sebagian besar game di Steam bertipe *short-session* atau memiliki replayability yang bervariasi.

---

## 📂 Struktur Repositori
```text
📁 gameverse-dashboard/
├── 📄 app.py                   # Kode utama aplikasi Streamlit
├── 📄 requirements.txt         # Daftar library Python yang dibutuhkan
├── 📄 README.md                # Dokumentasi proyek (file ini)
└── 📁 dataset/
    └── 📄 steam_clean.csv      # Dataset yang digunakan
