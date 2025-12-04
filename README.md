# 🦆 DuckDB SQL Analytics: School Data Analysis

Repository ini berisi demonstrasi penggunaan **DuckDB** (In-process OLAP Database) untuk melakukan analisis data pendidikan menggunakan perintah SQL modern.

Project ini mensimulasikan **Analytics Layer** dalam arsitektur Modern Data Stack. Script ini fokus pada transformasi dan analisis data yang sudah ter-materialisasi dalam format `Parquet`, meniru cara kerja **dbt (data build tool)** dalam mengelola data warehouse tanpa membebani infrastruktur server.

## 📊 Overview

Script ini mensimulasikan pekerjaan seorang **Data Analyst/Analytics Engineer** dalam mengolah data:

1.  **Data Filtering**: Menggunakan `SELECT` dan `WHERE` (Slicing & Dicing).
2.  **Aggregation**: Menggunakan `GROUP BY`, `COUNT`, dan `SUM` untuk statistik makro.
3.  **Comparative Analysis**: Mengimplementasikan logika SQL kompleks dengan **CTE (Common Table Expressions)** dan **JOIN** untuk membandingkan performa dua dataset kota (Benchmarking).

## 🛠️ Teknologi

* **Python 3.x**: Sebagai *orchestrator* untuk menjalankan query.
* **DuckDB**: Engine SQL kolom (columnar) yang sangat cepat, digunakan untuk memproses file Parquet secara lokal (*in-memory*).

## 📥 Sumber Data & Konsep Materialisasi

Dalam skenario dunia nyata (seperti penggunaan **dbt**), data mentah dari sumber (Raw Data) akan di-*materialized* terlebih dahulu menjadi format yang efisien sebelum dianalisis.

Repository ini mengasumsikan Anda sudah memiliki data yang telah diubah ke format `.parquet`.

👉 **Langkah 1: Ambil Data Mentah (Raw)**
Gunakan tool scraper yang telah saya sediakan di repository terpisah untuk mendapatkan data sekolah:
**[Link Repository Scraper (CSV Generator)](https://github.com/aldenputra222-prog/Scrapping-Data-from-Web)**

👉 **Langkah 2: Materialisasi Data**
Pastikan output CSV dari scraper tersebut disimpan/dikonversi menjadi format `.parquet`.
*(Ini mensimulasikan proses 'Bronze to Silver' layer dalam Data Engineering)*.

## 📂 Cara Menjalankan

1.  **Clone Repository Ini**
    ```bash
    git clone [https://github.com/aldenputra222-prog/DuckDB-School-Analytics.git](https://github.com/aldenputra222-prog/DuckDB-School-Analytics.git)
    cd DuckDB-School-Analytics
    ```

2.  **Siapkan Data (Staging)**
    * Pastikan file `data_yogyakarta.parquet` dan `data_bogor.parquet` sudah tersedia di dalam folder `result/`.
    * *Note: Script ini dirancang untuk membaca Parquet demi performa query sub-detik.*

3.  **Edit Konfigurasi (Opsional)**
    Jika nama file Anda berbeda, sesuaikan variabel di `analysis_duckdb.py`:
    ```python
    FILE_DATA_UTAMA    = 'result/nama_file_kamu.parquet'
    ```

4.  **Jalankan Analisis**
    ```bash
    python analysis_duckdb.py
    ```

## 🧠 Penjelasan Query SQL

### `Common Table Expression (CTE)`
Script ini menggunakan CTE (`WITH clause`) sebagai pengganti tabel fisik sementara. Ini mirip dengan konsep **Ephemeral Models** di dbt, di mana logika transformasi disimpan dalam memori untuk menjaga kebersihan *lineage* data.

### `Data Type Casting`
Menggunakan fungsi `TRY_CAST(column AS INTEGER)` untuk menangani inkonsistensi tipe data (*Dirty Data Handling*) secara *on-the-fly* saat query dijalankan.

---
**Disclaimer:** Project ini dibuat untuk tujuan edukasi, portofolio Data Engineering, dan demonstrasi SQL Logic.