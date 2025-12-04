import duckdb

# ==========================================
# ⚙️ KONFIGURASI FILE (UBAH BAGIAN INI)
# ==========================================
# Masukkan path/lokasi file Parquet hasil scraping kamu di sini.
# Pastikan file tersebut ada di folder yang sama atau sesuaikan path-nya.
FILE_DATA_UTAMA    = 'result/data_yogyakarta.parquet'  # Misal: Data Kota Yogyakarta
FILE_DATA_PEMBANDING = 'result/data_bogor.parquet'     # Misal: Data Kota Bogor (untuk Join)
# ==========================================

# Inisialisasi koneksi DuckDB (In-Memory)
con = duckdb.connect()

print(f"🚀 Memulai Analisis Menggunakan DuckDB...")
print(f"📂 File 1: {FILE_DATA_UTAMA}")
print(f"📂 File 2: {FILE_DATA_PEMBANDING}\n")

# ---------------------------------------------------------
# CASE 1: BASIC FILTERING (SELECT & WHERE)
# Tujuan: Mencari sekolah SD Negeri di dataset utama
# ---------------------------------------------------------
print("=== 1. CONTOH SELECT (FILTERING: SD NEGERI) ===")

query_select = f"""
    SELECT 
        Nama_Sekolah, 
        Kota_Kabupaten, 
        Peserta_Didik_Total 
    FROM '{FILE_DATA_UTAMA}' 
    WHERE Nama_Sekolah LIKE 'SD NEGERI%'
    LIMIT 5
"""

try:
    # .show() menampilkan hasil langsung di terminal dengan rapi
    con.sql(query_select).show()
except Exception as e:
    print(f"❌ Error pada Query 1: {e}")


# ---------------------------------------------------------
# CASE 2: AGGREGATION (GROUP BY)
# Tujuan: Menghitung total sekolah dan siswa per kota/kab
# ---------------------------------------------------------
print("\n=== 2. CONTOH GROUP BY (AGGREGATION) ===")

query_group = f"""
    SELECT 
        Kota_Kabupaten, 
        COUNT(*) as Jumlah_Sekolah, 
        SUM(TRY_CAST(Peserta_Didik_Total AS INTEGER)) as Total_Semua_Siswa
    FROM '{FILE_DATA_UTAMA}'
    WHERE Kota_Kabupaten IS NOT NULL 
    GROUP BY Kota_Kabupaten
    ORDER BY Total_Semua_Siswa DESC
"""

try:
    con.sql(query_group).show()
except Exception as e:
    print(f"❌ Error pada Query 2: {e}")


# ---------------------------------------------------------
# CASE 3: COMPLEX LOGIC (CTE & JOIN)
# Tujuan: Membandingkan rata-rata jumlah siswa antar dua kota (Head-to-Head)
# ---------------------------------------------------------
print("\n=== 3. FINAL BATTLE: ANALISIS KOMPARASI (JOIN & CASE WHEN) ===")

query_battle = f"""
    WITH 
    -- CTE 1: Rata-rata siswa di Kota Utama (File 1)
    stats_kota_a AS (
        SELECT 
            Bentuk_Pendidikan, 
            AVG(TRY_CAST(Peserta_Didik_Total AS INTEGER)) as Rata_A
        FROM '{FILE_DATA_UTAMA}'
        WHERE Bentuk_Pendidikan IN ('SD', 'SMP', 'SMA', 'SMK')
        GROUP BY Bentuk_Pendidikan
    ),
    
    -- CTE 2: Rata-rata siswa di Kota Pembanding (File 2)
    stats_kota_b AS (
        SELECT 
            Bentuk_Pendidikan, 
            AVG(TRY_CAST(Peserta_Didik_Total AS INTEGER)) as Rata_B
        FROM '{FILE_DATA_PEMBANDING}'
        WHERE Bentuk_Pendidikan IN ('SD', 'SMP', 'SMA', 'SMK')
        GROUP BY Bentuk_Pendidikan
    )

    -- MAIN QUERY: Menggabungkan kedua data
    SELECT 
        stats_kota_a.Bentuk_Pendidikan, 
        
        ROUND(stats_kota_a.Rata_A, 0) as Avg_Siswa_File_1,
        ROUND(stats_kota_b.Rata_B, 0) as Avg_Siswa_File_2,
        
        -- Logika CASE WHEN untuk memberi label otomatis
        CASE 
            WHEN stats_kota_b.Rata_B > stats_kota_a.Rata_A THEN 'File 2 Lebih Padat'
            WHEN stats_kota_b.Rata_B < stats_kota_a.Rata_A THEN 'File 1 Lebih Padat'
            ELSE 'Sama Kuat'
        END as Kesimpulan,

        -- Menghitung selisih absolut
        ABS(ROUND(stats_kota_b.Rata_B - stats_kota_a.Rata_A, 0)) as Selisih_Siswa
        
    FROM stats_kota_a
    JOIN stats_kota_b ON stats_kota_a.Bentuk_Pendidikan = stats_kota_b.Bentuk_Pendidikan
    
    ORDER BY stats_kota_a.Bentuk_Pendidikan
"""

try:
    con.sql(query_battle).show()
except Exception as e:
    print(f"❌ Error pada Query 3 (Pastikan kolom di kedua file sama): {e}")