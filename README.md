# 🦆 DuckDB SQL Analytics: School Data Analysis

> **Local Data Lakehouse Simulation** | *Build efficient data pipelines without a server.*

Repository ini mendemonstrasikan penggunaan **DuckDB** (In-process OLAP Database) dan prinsip **dbt** untuk membangun pipeline analisis data pendidikan yang ringan namun *powerful*.

Project ini mensimulasikan arsitektur **Local Data Lakehouse**, di mana proses *Storage*, *Compute*, dan *Transformation* dilakukan secara terpisah namun terintegrasi dalam satu lingkungan lokal.

## 📂 Struktur Project

Berikut adalah peta struktur file dalam repository ini:

```bash
📦 DuckDB-School-Analytics
 ┣ 📂 seeds/                 # Raw Data (Format CSV mentah)
 ┣ 📂 result/                # Data Lake Storage (Output file .parquet)
 ┣ 📜 analysis_csv.py        # Analytics Layer (CSV)
 ┣ 📜 analysis_duckdb.py     # Analytics Layer (Parquet)
 ┣ 📜 export_to_parquet.sql  # Transformation Layer (Logika konversi CSV ke Parquet)
 ┗ 📜 README.md              # Dokumentasi Project
```

## 🛠️ Alur Kerja (Workflow)
Repository ini mendemonstrasikan dua tahapan utama dalam Data Engineering Lifecycle:

1. Data Transformation (ELT)
File export_to_parquet.sql merepresentasikan layer Transformation. Di fase ini, data mentah dibersihkan dan diubah menjadi format Parquet agar hemat penyimpanan dan mempercepat proses baca (I/O).

--- Simulasi Model dbt (export_to_parquet.sql)
```bash
COPY (
    SELECT 
        nama_sekolah,
        CAST(jumlah_siswa AS INTEGER) as total_siswa,
        kota_administrasi
    FROM read_csv_auto('seeds/raw_school_data.csv')
    WHERE jumlah_siswa IS NOT NULL
) TO 'result/data_bogor.parquet' (FORMAT 'PARQUET');
```
Input: CSV dari folder seeds/.

Output: File .parquet yang tersimpan di folder result/.

2. Data Analytics
Setelah data matang (Parquet), script analysis_duckdb.py bertindak sebagai Consumer. Script ini menggunakan kekuatan DuckDB untuk:

✅ Melakukan Filtering (WHERE) & Aggregation (GROUP BY).

⚡ Memproses file Parquet secara instan (sub-second query performance).

🔄 Melakukan komparasi data antar kota menggunakan CTE dan JOIN.

Rasakan perbedaan kecepatannya! Script ini membuktikan betapa powerful-nya kombinasi DuckDB dan Parquet dibandingkan pembacaan CSV biasa. Jalankan analysis_csv.py lalu analysis_duckdb.py, dan lihat bagaimana query modern memangkas waktu proses secara drastis.

## 🚀 Cara Menjalankan
Ikuti langkah-langkah berikut untuk mencoba project ini di komputer Anda:

1. Clone Repository
Buka terminal dan jalankan perintah berikut:
git clone https://github.com/aldenputra222-prog/DuckDB-School-Analytics.git
cd DuckDB-School-Analytics

2. Siapkan Data (Materialization)
Pastikan file Parquet sudah tersedia di folder result/. (Dalam skenario nyata, file ini dihasilkan oleh dbt run atau script ingestion).

3. Jalankan Analisis
Jalankan script Python untuk melihat hasil benchmark dan analisis data sekolah:
python analysis_duckdb.py

📝 Disclaimer
Project ini dibuat untuk tujuan edukasi, portofolio Data Engineering, dan demonstrasi implementasi Local Data Lakehouse sederhana.