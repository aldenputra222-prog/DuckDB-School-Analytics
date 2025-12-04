# 🦆 DuckDB SQL Analytics: School Data Analysis

Repository ini berisi demonstrasi penggunaan **DuckDB** (In-process OLAP Database) untuk melakukan analisis data pendidikan menggunakan perintah SQL modern. 

Tujuan dari project ini adalah menunjukkan bagaimana mengolah file `Parquet` secara langsung tanpa perlu loading ke database server tradisional, menghasilkan performa analisis yang sangat cepat (sub-second latency).

## 📊 Overview

Script ini mensimulasikan pekerjaan seorang **Data Analyst** dalam mengolah data mentah menjadi insight, mencakup:

1.  **Data Filtering**: Menggunakan `SELECT` dan `WHERE` untuk memfilter data spesifik.
2.  **Aggregation**: Menggunakan `GROUP BY`, `COUNT`, dan `SUM` untuk melihat statistik makro.
3.  **Complex Logic**: Mengimplementasikan **CTE (Common Table Expressions)** dan **JOIN** untuk membandingkan performa dua dataset berbeda (Comparative Analysis).

## 🛠️ Teknologi

* **Python 3.x**
* **DuckDB**: "SQLite for Analytics" - database kolom yang sangat cepat.

## 📂 Cara Menggunakan

1.  **Siapkan Data Parquet**
    Pastikan kamu memiliki dua file data (format `.parquet` atau `.csv`) yang ingin dianalisis. *Jika belum punya, kamu bisa menggunakan script scraper di repository saya yang lain.*

2.  **Edit Konfigurasi**
    Buka file `analysis_duckdb.py` dan ubah bagian ini sesuai lokasi file kamu:

    ```python
    FILE_DATA_UTAMA    = 'path/to/data_jakarta.parquet'
    FILE_DATA_PEMBANDING = 'path/to/data_surabaya.parquet'
    ```

3.  **Jalankan Script**
    ```bash
    python analysis_duckdb.py
    ```

## 🧠 Penjelasan Query SQL

### `Common Table Expression (CTE)`
Script ini menggunakan CTE (`WITH clause`) untuk membuat tabel sementara dalam memori. Ini membuat kode lebih mudah dibaca (readable) dan modular dibandingkan *nested subqueries*.

### `Data Type Casting`
Karena data mentah seringkali berupa string, saya menggunakan fungsi `TRY_CAST(column AS INTEGER)` dari DuckDB untuk memastikan proses kalkulasi angka berjalan aman tanpa error jika ada data kotor.

---
**Disclaimer:** Project ini dibuat untuk tujuan edukasi dan portofolio Data Analysis.