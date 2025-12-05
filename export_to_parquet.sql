{{ config(
    materialized='external',
    location='target/data_bogor.parquet' --tujuan
) }}

SELECT *
FROM {{ ref('data_bogor.csv') }} --namafilecsv