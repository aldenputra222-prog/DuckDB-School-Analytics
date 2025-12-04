# 🦆 DuckDB SQL Analytics: School Data Analysis

Repository ini demonstrasi penggunaan **DuckDB** (In-process OLAP Database) untuk melakukan analisis data pendidikan menggunakan perintah SQL modern. 

Tujuan project ini adalah membuktikan efisiensi pengolahan data lokal. Kita dapat mengolah file `Parquet` secara langsung tanpa perlu loading ke database server tradisional (seperti MySQL/PostgreSQL), menghasilkan performa analisis dengan *sub-second latency*.

## 📊 Overview

Script ini mensimulasikan alur kerja seorang **Data Analyst** dalam mengubah data mentah menjadi *actionable insights*:

1.  **Data Filtering**: Menggunakan `SELECT` dan `WHERE` untuk memfilter entitas sekolah spesifik.
2.  **Aggregation**: Menggunakan `GROUP BY`, `COUNT`, dan `SUM` untuk rekapitulasi statistik makro.
3.  **Comparative Analysis**: Mengimplementasikan **CTE (Common Table Expressions)** dan **JOIN** untuk membandingkan kepadatan siswa antara dua kota secara *head-to-head*.
4.  **Robustness**: Script dilengkapi fitur pengecekan file otomatis untuk memastikan integritas data sebelum analisis dimulai.

## 🛠️ Teknologi

* **Python 3.x**: Bahasa pemrograman utama.
* **DuckDB**: "SQLite for Analytics" - database kolom (columnar) yang sangat cepat untuk analisis query.

## 📥 Sumber Data (Data Source)

Script ini membutuhkan file dataset dalam format `.parquet` atau `.csv`. 
Agar analisis berjalan, Anda membutuhkan data sekolah yang valid. Saya telah menyediakan tools untuk mengambil data tersebut secara otomatis di repository terpisah:

👉 **[Ambil Data Sekolah via Scraper Di Sini](https://github.com/aldenputra222-prog/Scrapping-Data-from-Web)**

## 📂 Cara Menjalankan

1.  **Clone Repository Ini**
    ```bash
    git clone [https://github.com/aldenputra222-prog/DuckDB-School-Analytics.git](https://github.com/aldenputra222-prog/DuckDB-School-Analytics.git)
    cd DuckDB-School-Analytics
    ```

2.  **Siapkan Data**
    * Jalankan tool scraper di link di atas untuk mendapatkan data kota (misal: Yogyakarta dan Bogor).
    * Pindahkan file hasil scraping (format `.parquet` atau `.csv`) ke dalam folder `result/` di project ini.
    * *Note: Pastikan nama file sesuai dengan konfigurasi di script (default: `data_yogyakarta.parquet` dan `data_bogor.parquet`).*

3.  **Jalankan Analisis**
    ```bash
    python analysis_duckdb.py
    ```

## 🧠 Penjelasan Query SQL

### `Common Table Expression (CTE)`
Script ini menggunakan CTE (`WITH clause`) untuk menstrukturisasi query yang kompleks menjadi bagian-bagian modular. Ini membuat logika "Comparative Analysis" lebih mudah dibaca dan dipelihara.

### `Data Type Casting`
Data mentah dari web seringkali bertipe string/text. Saya menggunakan fungsi `TRY_CAST(column AS INTEGER)` untuk memastikan proses kalkulasi angka berjalan aman (tanpa error/crash) meskipun terdapat data kotor (*dirty data*).

---
**Disclaimer:** Project ini dibuat untuk tujuan edukasi, portofolio Data Engineering, dan Data Analysis.