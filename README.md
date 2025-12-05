🦆 DuckDB SQL Analytics: School Data Analysis
Repository ini berisi demonstrasi penggunaan DuckDB (In-process OLAP Database) dan dbt untuk membangun pipeline analisis data pendidikan.

Project ini mensimulasikan arsitektur Local Data Lakehouse, di mana transformasi data dan analisis dilakukan secara terpisah namun terintegrasi.

📂 Struktur Project
analysis_duckdb.py: Script Python utama untuk melakukan query analisis (Analytics Layer).

export_to_parquet.sql: File model SQL (simulasi dbt) yang mendefinisikan logika transformasi data mentah ke format Parquet.

seeds/: Folder tempat menyimpan Raw Data. (csv)

result/: Folder output (Data Lake) tempat file Parquet disimpan.

🛠️ Alur Kerja (Workflow)
Repository ini mendemonstrasikan dua tahapan utama dalam Data Engineering:

1. Data Transformation (export_to_parquet.sql)
File ini merepresentasikan layer Transformation. Di sinilah data mentah dibersihkan dan diubah menjadi format Parquet.

SQL

-- Cuplikan logika dari export_to_parquet.sql
{{ config(
    materialized='external',
    location='target/data_Bogor.parquet'
) }}
...
Fungsi: Mengubah data CSV menjadi format columnar (Parquet) agar hemat penyimpanan dan cepat dibaca.

Output: Menghasilkan file .parquet di folder target.

2. Data Analytics (analysis_duckdb.py)
Setelah data diubah menjadi Parquet, script Python ini bertindak sebagai Consumer.

Melakukan filtering (WHERE) & Aggregation (GROUP BY).

Menggunakan DuckDB untuk memproses file Parquet tersebut secara instan (sub-second query).

Melakukan komparasi data antar kota menggunakan CTE dan JOIN.

📥 Cara Menjalankan
Clone Repository

Bash

git clone https://github.com/aldenputra222-prog/DuckDB-School-Analytics.git
cd DuckDB-School-Analytics
Siapkan Data Pastikan file Parquet sudah tersedia di folder result/ (dihasilkan dari proses transformasi sebelumnya).

Jalankan Analisis

Bash

python analysis_duckdb.py
Disclaimer: Project ini dibuat untuk tujuan edukasi, portofolio Data Engineering, dan demonstrasi implementasi Local Data Lakehouse sederhana.