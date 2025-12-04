import duckdb
import os
import sys

# ==========================================
# ⚙️ KONFIGURASI OTOMATIS
# ==========================================
# Script akan mencari file di folder 'result' atau folder saat ini
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'result') # Asumsi data ada di folder result

# Nama file target (Pastikan nama ini sesuai dengan hasil output scraper kamu)
FILE_1_NAME = 'data_yogyakarta.parquet'
FILE_2_NAME = 'data_bogor.parquet'

# Path lengkap otomatis
FILE_DATA_UTAMA    = os.path.join(DATA_DIR, FILE_1_NAME)
FILE_DATA_PEMBANDING = os.path.join(DATA_DIR, FILE_2_NAME)

# ==========================================
# 🛠️ FUNGSI UTILITAS (Supaya script tidak crash)
# ==========================================
def check_files():
    """Mengecek keberadaan file data sebelum analisis dimulai."""
    files_missing = []
    if not os.path.exists(FILE_DATA_UTAMA):
        files_missing.append(FILE_DATA_UTAMA)
    if not os.path.exists(FILE_DATA_PEMBANDING):
        files_missing.append(FILE_DATA_PEMBANDING)
    
    if files_missing:
        print("\n⚠️  PERINGATAN: DATA TIDAK DITEMUKAN!")
        print("="*50)
        print("Script ini membutuhkan file data hasil scraping.")
        print(f"File yang hilang: {files_missing}")
        print("\nSOLUSI:")
        print("1. Jalankan script scraper di repo sebelah.")
        print("2. Pindahkan file .parquet/.csv hasil scraping ke folder 'result/'.")
        print("="*50)
        sys.exit(1) # Berhenti dengan rapi

# Jalankan pengecekan file dulu
check_files()

# ==========================================
# 🚀 MULAI ANALISIS DUCKDB
# ==========================================
# DuckDB berjalan 'In-Memory', artinya sangat cepat karena tidak perlu setup server.
con = duckdb.connect()

print(f"\n🚀 Memulai Analisis Data Pendidikan...")
print(f"✅ Data 1 Loaded: {FILE_1_NAME}")
print(f"✅ Data 2 Loaded: {FILE_2_NAME}\n")

# ---------------------------------------------------------
# CASE 1: BASIC FILTERING (SQL Dasar)
# Penjelasan: Mengambil irisan data spesifik (Slicing/Dicing).
# Mengapa pakai DuckDB? Karena bisa query langsung ke file tanpa 'INSERT' ke DB.
# ---------------------------------------------------------
print("=== 1. FILTERING DATA (Mencari SD Negeri) ===")
print("Query: SELECT ... WHERE ... LIKE ...")

query_select = f"""
    SELECT 
        Nama_Sekolah, 
        Kecamatan,
        Peserta_Didik_Total 
    FROM '{FILE_DATA_UTAMA}' 
    WHERE Nama_Sekolah LIKE 'SD NEGERI%' 
      AND Kecamatan IS NOT NULL
    ORDER BY Peserta_Didik_Total DESC
    LIMIT 5
"""

try:
    con.sql(query_select).show()
except Exception as e:
    print(f"❌ Error Query 1: {e}")


# ---------------------------------------------------------
# CASE 2: AGGREGATION (Statistik Deskriptif)
# Penjelasan: Melakukan 'Zoom Out' untuk melihat gambaran besar (Macro View).
# Menggunakan TRY_CAST untuk menangani data kotor (misal ada teks di kolom angka).
# ---------------------------------------------------------
print("\n=== 2. AGGREGATION (Total Siswa per Kecamatan) ===")
print("Query: GROUP BY, COUNT, SUM, TRY_CAST")

query_group = f"""
    SELECT 
        Kecamatan, 
        COUNT(*) as Jumlah_Sekolah, 
        -- Mengubah string ke integer dengan aman (jika gagal jadi NULL, tidak error)
        SUM(TRY_CAST(Peserta_Didik_Total AS INTEGER)) as Total_Siswa
    FROM '{FILE_DATA_UTAMA}'
    WHERE Kecamatan IS NOT NULL 
    GROUP BY Kecamatan
    ORDER BY Total_Siswa DESC
    LIMIT 5
"""

try:
    con.sql(query_group).show()
except Exception as e:
    print(f"❌ Error Query 2: {e}")


# ---------------------------------------------------------
# CASE 3: COMPARATIVE ANALYSIS (Head-to-Head)
# Penjelasan: Analisis tingkat lanjut membandingkan 2 dataset berbeda.
# Teknik:
# 1. CTE (Common Table Expression): Membuat tabel sementara di memori agar kodingan rapi.
# 2. JOIN: Menggabungkan data Bogor & Yogya berdasarkan jenjang pendidikan.
# 3. CASE WHEN: Membuat logika bisnis (kesimpulan otomatis) di dalam query.
# ---------------------------------------------------------
print("\n=== 3. FINAL BATTLE: KOMPARASI KEPADATAN SISWA ===")
print("Query: CTE (WITH), JOIN, CASE WHEN Logic")

query_battle = f"""
    WITH 
    -- [CTE 1] Siapkan Rata-rata Kota A (Yogya)
    stats_kota_a AS (
        SELECT 
            Bentuk_Pendidikan, 
            AVG(TRY_CAST(Peserta_Didik_Total AS INTEGER)) as Rata_A
        FROM '{FILE_DATA_UTAMA}'
        WHERE Bentuk_Pendidikan IN ('SD', 'SMP', 'SMA', 'SMK')
        GROUP BY Bentuk_Pendidikan
    ),
    
    -- [CTE 2] Siapkan Rata-rata Kota B (Bogor)
    stats_kota_b AS (
        SELECT 
            Bentuk_Pendidikan, 
            AVG(TRY_CAST(Peserta_Didik_Total AS INTEGER)) as Rata_B
        FROM '{FILE_DATA_PEMBANDING}'
        WHERE Bentuk_Pendidikan IN ('SD', 'SMP', 'SMA', 'SMK')
        GROUP BY Bentuk_Pendidikan
    )

    -- [MAIN QUERY] Pertemukan kedua data (JOIN)
    SELECT 
        stats_kota_a.Bentuk_Pendidikan, 
        
        -- Bulatkan angka desimal agar rapi
        ROUND(stats_kota_a.Rata_A, 0) as 'Avg Siswa (File 1)',
        ROUND(stats_kota_b.Rata_B, 0) as 'Avg Siswa (File 2)',
        
        -- Logika Penentuan Pemenang (Insight Otomatis)
        CASE 
            WHEN stats_kota_b.Rata_B > stats_kota_a.Rata_A THEN 'File 2 Lebih Padat'
            WHEN stats_kota_b.Rata_B < stats_kota_a.Rata_A THEN 'File 1 Lebih Padat'
            ELSE 'Seimbang'
        END as Kesimpulan,

        ABS(ROUND(stats_kota_b.Rata_B - stats_kota_a.Rata_A, 0)) as Selisih
        
    FROM stats_kota_a
    JOIN stats_kota_b ON stats_kota_a.Bentuk_Pendidikan = stats_kota_b.Bentuk_Pendidikan
    
    ORDER BY stats_kota_a.Bentuk_Pendidikan ASC
"""

try:
    con.sql(query_battle).show()
except Exception as e:
    print(f"❌ Error Query 3: {e}")