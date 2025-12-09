import pandas as pd
import time
import numpy as np
import os

print("\n" + "="*40)
print("   BENCHMARK PANDAS + CSV (Traditional)")
print("="*40 + "\n")

file_yogya = 'seeds/data_Yogyakarta.csv'
file_bogor = 'seeds/data_Bogor.csv'

def safe_read_csv(file_path):
    return pd.read_csv(file_path, sep=None, engine='python', on_bad_lines='skip')

if not os.path.exists(file_yogya) or not os.path.exists(file_bogor):
    print(f"❌ ERROR: File tidak ditemukan di folder 'seeds'.")
    exit()

# ==========================================
# 1. TEST SELECT
# ==========================================
print("=== 1. TEST SELECT (Mencari Sekolah di Kota Yogya) ===")
try:
    start_time = time.time()
    
    df_yogya = safe_read_csv(file_yogya)
    
    df_filtered = df_yogya[
        (df_yogya['Kota_Kabupaten'] == 'Kota Yogyakarta') & 
        (df_yogya['Nama_Sekolah'].str.contains('SD NEGERI', na=False, case=False))
    ]
    
    result = df_filtered[['Nama_Sekolah', 'Kota_Kabupaten', 'Peserta_Didik_Total']].head(5)
    print(result.to_string(index=False)) 
    
    end_time = time.time()
    print(f"✅ STATUS: SUKSES | ⏱️ WAKTU : {end_time - start_time:.5f} detik")
except Exception as e:
    print(f"❌ Error SELECT: {e}")

# ==========================================
# 2. TEST GROUP BY
# ==========================================
print("\n=== 2. TEST GROUP BY (Menghitung Total Siswa per Kota) ===")
try:
    start_time = time.time()
    
    df = safe_read_csv(file_yogya)
    
    df['Peserta_Didik_Total'] = pd.to_numeric(df['Peserta_Didik_Total'], errors='coerce').fillna(0)
    
    grouped = df.groupby('Kota_Kabupaten').agg(
        Jumlah_Sekolah=('Kota_Kabupaten', 'count'),
        Total_Semua_Siswa=('Peserta_Didik_Total', 'sum')
    ).reset_index()
    
    grouped = grouped.sort_values(by='Total_Semua_Siswa', ascending=False)
    print(grouped.to_string(index=False))
    
    end_time = time.time()
    print(f"✅ STATUS: SUKSES | ⏱️ WAKTU : {end_time - start_time:.5f} detik")
except Exception as e:
    print(f"❌ Error GROUP BY: {e}")

# ==========================================
# 3. TEST JOIN
# ==========================================
print("\n=== 3. TEST JOIN (Membandingkan Data Yogya vs Bogor) ===")
try:
    start_time = time.time()
    
    df_y = safe_read_csv(file_yogya)
    df_b = safe_read_csv(file_bogor)
    
    df_y['Peserta_Didik_Total'] = pd.to_numeric(df_y['Peserta_Didik_Total'], errors='coerce')
    stats_yogya = df_y.groupby('Bentuk_Pendidikan')['Peserta_Didik_Total'].mean().reset_index()
    stats_yogya.rename(columns={'Peserta_Didik_Total': 'Rata_Yogya'}, inplace=True)
    
    df_b['PD_Total'] = pd.to_numeric(df_b['PD_Total'], errors='coerce')
    stats_bogor = df_b.groupby('Bentuk_Pendidikan')['PD_Total'].mean().reset_index()
    stats_bogor.rename(columns={'PD_Total': 'Rata_Bogor'}, inplace=True)
    
    merged = pd.merge(stats_yogya, stats_bogor, on='Bentuk_Pendidikan', how='inner')
    
    conditions = [(merged['Rata_Bogor'] > merged['Rata_Yogya']), (merged['Rata_Bogor'] < merged['Rata_Yogya'])]
    choices = ['Bogor Lebih Padat', 'Yogya Lebih Padat']
    merged['Kesimpulan'] = np.select(conditions, choices, default='Sama Kuat')
    
    merged['Selisih_Siswa'] = (merged['Rata_Bogor'] - merged['Rata_Yogya']).abs().round(0)
    
    print(merged[['Bentuk_Pendidikan', 'Kesimpulan', 'Selisih_Siswa']].sort_values('Bentuk_Pendidikan').to_string(index=False))
    
    end_time = time.time()
    print(f"✅ STATUS: SUKSES | ⏱️ WAKTU : {end_time - start_time:.5f} detik")
except Exception as e:
    print(f"❌ Error JOIN: {e}")